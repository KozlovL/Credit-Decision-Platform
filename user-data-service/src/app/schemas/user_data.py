from datetime import date, datetime, UTC
from typing import Self, Any

from common.constants import CreditStatus
from common.schemas.user import UserPhoneWrite, ProfileWrite
from pydantic import (
    BaseModel, PositiveInt, model_validator, ConfigDict,
    field_validator,
)

from app.constants import LOAN_ID_REGEX


class ValidateStatusAndCloseDateMixin:
    """Миксин с валидацией статуса и даты закрытия кредита."""
    close_date: Any
    status: Any

    @model_validator(mode='after')
    def validate_status_close_date(self) -> Self:
        """Валидация поля close_date относительно статуса."""
        if (
            (
                self.close_date is None
                and self.status != CreditStatus.OPEN
            )
            or
                (
                    self.close_date is not None
                    and self.status != CreditStatus.CLOSED
                )
        ):
            raise ValueError(
                'Поле close_date может быть пустым только при открытом '
                'статусе кредита и наоборот.'
            )
        return self


class CreditHistoryRead(
    BaseModel,
    ValidateStatusAndCloseDateMixin,
):
    """Схема кредитной истории для чтения."""

    loan_id: str
    product_name: str
    amount: PositiveInt
    issue_date: date
    term_days: PositiveInt
    status: CreditStatus
    close_date: date | None

    @field_validator('loan_id')
    def validate_phone(cls, value: str) -> str | None:
        if not LOAN_ID_REGEX.match(value):
            raise ValueError(
                'Неверный формат loan_id. '
                'Верный формат выглядит так - loan_YYYY-MM-DD_ID'
            )
        return value


class UserDataRead(UserPhoneWrite):
    """Схема данных пользователя для чтения."""

    profile: ProfileWrite
    history: list[CreditHistoryRead]


class LoanCreateOrUpdate(CreditHistoryRead):
    """Схема для создания или обновления записи в кредитной истории."""

    product_name: str | None = None
    amount: PositiveInt | None = None
    issue_date: date | None = None
    term_days: PositiveInt | None = None
    status: CreditStatus
    close_date: date | None = None

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')

    @field_validator('issue_date', 'close_date')
    def validate_dates(cls, value: date) -> date:
        """Валидация дат: дата не может быть в будущем."""
        if value is not None and value > datetime.now(UTC).date():
            raise ValueError('Несуществующая дата.')
        return value

    @model_validator(mode='after')
    def validate_close_after_issue(self):
        """Проверки даты закрытия относительно даты открытия."""
        if self.close_date is not None and self.issue_date is not None:
            if self.close_date < self.issue_date:
                raise ValueError(
                        'Дата закрытия не может быть раньше даты выдачи.'
                    )
        return self


class LoanCreate(CreditHistoryRead):
    """Схема для создания записи в кредитной истории."""

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')


class LoanUpdate(
    BaseModel,
    ValidateStatusAndCloseDateMixin,
):
    """Схема для обновления записи в кредитной истории."""

    loan_id: str
    status: CreditStatus
    close_date: date | None

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')
