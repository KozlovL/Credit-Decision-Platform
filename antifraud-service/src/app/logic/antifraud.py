from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import UTC, datetime, timedelta

import redis
from common.constants import (
    CREDIT_EXPIRATION_DAYS,
    AgeType,
    CreditStatus,
    EmploymentType,
    MonthlyIncomeType,
)
from common.schemas.user import CreditHistoryRead, ProfileWrite
from fastapi import HTTPException
from starlette import status

from app.clients.redis_client import RedisClient
from app.constants import (
    MAX_APPLICATIONS_PER_DAY,
    SIGNIFICANT_INCOME_DECREASE,
    SIGNIFICANT_INCOME_INCREASE,
    DecisionType,
    RejectionReasonType,
)

logger = logging.getLogger('uvicorn')

class AntifraudBase(ABC):
    """Базовый класс антифрод проверок."""

    def __init__(self, current_profile: ProfileWrite, phone: str):
        self.phone = phone
        self.current_profile = current_profile
        self.reasons: list[str] = []

    def check_min_age(self) -> None:
        """Проверка на минимальный возраст."""
        if self.current_profile.age < AgeType.ADULT_AGE.value:
            self.reasons.append(
                RejectionReasonType.MIN_AGE.format(
                    user_age=self.current_profile.age,
                    min_age=AgeType.ADULT_AGE.value
                )
            )

    def check_min_income(self) -> None:
        """Проверка на минимальный доход."""
        if self.current_profile.monthly_income < MonthlyIncomeType.LOW_INCOME.value:
            self.reasons.append(
                RejectionReasonType.MIN_INCOME.format(
                    user_income=self.current_profile.monthly_income,
                    min_income=MonthlyIncomeType.LOW_INCOME.value
                )
            )

    def check_employment_status(self) -> None:
        """Проверка на статус трудоустройства."""
        if self.current_profile.employment_type == EmploymentType.UNEMPLOYED:
            self.reasons.append(
                RejectionReasonType.EMPLOYMENT_STATUS.format(
                    employment_type=self.current_profile.employment_type.value
                )
            )

    @abstractmethod
    async def run_checks(self) -> tuple[str, list[str]]:
        """Метод должен быть реализован в наследниках и запускать все проверки."""


class AntifraudPioneer(AntifraudBase):
    """Антифрод для первичника."""

    def __init__(
            self,
            redis_client: RedisClient,
            current_profile: ProfileWrite,
            phone: str
        ):
        super().__init__(current_profile=current_profile, phone=phone)
        self.redis = redis_client

    async def check_daily_application_limit(self) -> None:
        """Проверка на кол-во заявок за сутки."""
        try:
            phone = self.phone
            key = f'pioneer:applications:{phone}'
            events = await self.redis.get_events(key)
            count = len(events)
            if count >= MAX_APPLICATIONS_PER_DAY:
                self.reasons.append(
                    RejectionReasonType.DAILY_APPLICATION_LIMIT.format(
                        count=count,
                        max_allowed=MAX_APPLICATIONS_PER_DAY
                    )
                )
            await self.redis.add_event_zset(key)
            logger.info(
                f'Новая запись добавлена для телефона {phone}, '
                f'всего записей: {count + 1}'
            )
        except redis.RedisError as err:
            logger.error(f'Redis недоступен: {err}')
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(err)
            ) from err

    def check_property_with_low_income(self) -> None:
        """Проверка на наличие недвижимости при среднем доходе."""
        if (
            self.current_profile.has_property is True
            and self.current_profile.monthly_income < MonthlyIncomeType.AVERAGE_INCOME
        ):
            self.reasons.append(
                RejectionReasonType.PROPERTY_WITH_LOW_INCOME.format(
                    user_income=self.current_profile.monthly_income,
                    income_threshold=MonthlyIncomeType.AVERAGE_INCOME.value
                )
            )

    async def run_checks(self) -> tuple[str, list[str]]:
        """Запуск проверок."""
        self.check_min_age()
        self.check_min_income()
        self.check_employment_status()
        await self.check_daily_application_limit()
        self.check_property_with_low_income()
        decision = (
            DecisionType.PASSED.value if not self.reasons
            else DecisionType.REJECTED.value
        )
        return decision, self.reasons


class AntifraudRepeater(AntifraudBase):
    """Антифрод для повторника."""

    def __init__(
        self,
        current_profile: ProfileWrite,
        credit_history: list[CreditHistoryRead],
        previous_profile: ProfileWrite,
        phone: str
    ):
        super().__init__(current_profile=current_profile, phone=phone)
        self.credit_history = credit_history
        self.previous_profile = previous_profile
        # Определяем дату последнего кредита
        self.last_credit_date = max(
            credit_note.issue_date for credit_note in self.credit_history
        )

    def check_overdue_loans(self) -> None:
        """Метод проверки просроченных кредитов."""
        # Проходим по всем записям
        for credit_note in self.credit_history:
            # Если кредит закрыт, то идем на следующую итерацию
            if credit_note.status is CreditStatus.OVERDUE:
                self.reasons.append(RejectionReasonType.OVERDUE_LOANS)
                break

    def check_significant_income_change(self) -> None:
        """Проверяет резкое изменение дохода."""
        prev_income = self.previous_profile.monthly_income
        curr_income = self.current_profile.monthly_income

        change_ratio = curr_income / prev_income

        if (
            change_ratio >= SIGNIFICANT_INCOME_INCREASE
            or change_ratio <= SIGNIFICANT_INCOME_DECREASE
        ):
            change_percent = round((change_ratio - 1) * 100)
            self.reasons.append(
                RejectionReasonType.SIGNIFICANT_INCOME_CHANGE.format(
                    prev_income=prev_income,
                    current_income=curr_income,
                    change_percent=change_percent
                )
            )


    def check_employment_change(self) -> None:
        """Проверка изменения типа трудоустройства."""
        prev_type = self.previous_profile.employment_type
        curr_type = self.current_profile.employment_type
        if (
            prev_type == EmploymentType.FULL_TIME
            and curr_type != EmploymentType.FULL_TIME
        ):
            self.reasons.append(
                RejectionReasonType.EMPLOYMENT_CHANGE_NOT_ALLOWED.format(
                    current_employment_type=curr_type
                )
            )

    async def run_checks(self) -> tuple[str, list[str]]:
        """Вызов всех проверок."""
        self.check_min_age()
        self.check_min_income()
        self.check_employment_status()
        self.check_overdue_loans()
        # Проверка применения правил R2 только если последний кредит <= 30 дней
        if (datetime.now(UTC).date() - self.last_credit_date).days <= 30:
            self.check_significant_income_change()
            self.check_employment_change()
        decision = (
            DecisionType.PASSED.value if not self.reasons
            else DecisionType.REJECTED.value
        )
        return decision, self.reasons
