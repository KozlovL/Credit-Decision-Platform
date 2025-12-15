from datetime import UTC, datetime, timedelta
from typing import Any

from common.constants import (
    AgeType,
    EmploymentType,
    LastCreditAmountTypes,
    MonthlyIncomeType,
)
from common.schemas.product import ProductWrite
from common.schemas.user import CreditHistoryRead, UserDataPhoneWrite

from app.clients.antifraud_service_client import AntifraudServiceClient
from app.constants import (
    ACCEPTED_STR,
    FIRST_CREDIT_DAYS_TO_GET_SCORE,
    MIN_PIONEER_SCORE_FOR_PRODUCT,
    MIN_REPEATER_SCORE_FOR_PRODUCT,
    REJECTED_STR,
)
from app.repository.product import (
    get_available_pioneer_products_with_score,
    get_available_repeater_products_with_score,
)


class ScoringBase:
    """Базовый класс скоринга."""

    def __init__(
            self,
            antifraud_service_client: AntifraudServiceClient,
            user_data: UserDataPhoneWrite,
            available_products_with_score: dict[str, int],
            min_score_for_acceptance: int,
            products: list[ProductWrite],
            credit_history: list[CreditHistoryRead] | None = None,
    ):
        self.user_data = user_data
        self.available_products_with_score = available_products_with_score
        self.min_score_for_acceptance = min_score_for_acceptance
        self.credit_history = credit_history
        self.products = products
        self.antifraud_service_client = antifraud_service_client

    def immediate_rejection(self) -> Any:
        """Метод проверки немедленного отказа."""
        return True

    def score_age(self, age: int) -> int:
        """Метод скоринга возраста."""
        if age < AgeType.AVERAGE_AGE:
            score = 1
        elif age < AgeType.OLD_AGE:
            score = 3
        else:
            score = 2
        return score

    def score_monthly_income(self, monthly_income: int) -> int:
        """Метод скоринга ежемесячного дохода."""
        if monthly_income < MonthlyIncomeType.AVERAGE_INCOME:
            score = 1
        elif monthly_income < MonthlyIncomeType.HIGH_INCOME:
            score = 2
        else:
            score = 3
        return score

    def score_employment_type(self, employment_type: str) -> int:
        """Метод скоринга типа занятости."""
        if employment_type == EmploymentType.FULL_TIME:
            return 3
        if employment_type == EmploymentType.FREELANCE:
            return 1
        return 0

    def score_property(self, has_property: bool) -> int:
        """Метод скоринга недвижимости."""
        return 2 if has_property else 0

    def scoring_credit_history(self) -> int:
        """Метод скоринга кредитной истории."""
        credit_history = self.credit_history
        # Если кредитная история отсутствует, то возвращаем 0
        if credit_history is None:
            return 0
        first_note = credit_history[0]
        last_note_amount = credit_history[-1].amount
        score = 0
        # Если первый кредит был взят больше года назад, возвращаем 3
        if (
                datetime.now(UTC).date() - first_note.issue_date
                > timedelta(days=FIRST_CREDIT_DAYS_TO_GET_SCORE)
        ):
            score += 3
        # Если сумма последнего кредита меньше 50000, возвращаем 1
        if last_note_amount < LastCreditAmountTypes.LOW_AMOUNT:
            score += 1
        # Если сумма последнего кредита меньше 100000, возвращаем 2
        elif last_note_amount < LastCreditAmountTypes.AVERAGE_AMOUNT:
            score += 2
        # Иначе возвращаем 3
        else:
            score += 3
        return score

    def scoring_process(self) -> int:
        """Метод скоринга пользователя."""
        user_data = self.user_data
        score = 0
        score += self.score_age(user_data.age)
        score += self.score_monthly_income(user_data.monthly_income)
        score += self.score_employment_type(user_data.employment_type)
        score += self.score_property(user_data.has_property)
        score += self.scoring_credit_history()
        return score

    def check_products_with_score(
            self,
            products: list[ProductWrite],
            user_score: int,
    ) -> ProductWrite | None:
        """Метод проверки доступности продуктов с учётом скоринга."""
        if user_score < self.min_score_for_acceptance:
            return None
        current_product = None
        # Для каждого продукта в списке...
        for new_product in products:
            # Получаем его оценку
            new_product_score = self.available_products_with_score[
                new_product.name
            ]
            # Если пользователю хватает баллов...
            if user_score >= new_product_score:
                # Если его текущий продукт лучше...
                if (
                        current_product is not None
                        and (
                        self.available_products_with_score[
                            current_product.name
                        ]
                        >= new_product_score
                        )
                ):
                    # Переходим на следующую итерацию...
                    continue
                # Иначе предлагаем новый продукт
                current_product = new_product
        return current_product

    def get_answer_for_score(self) -> tuple[str, ProductWrite | None]:
        """
        Метод получения ответа по скорингу.

        Возвращает кортеж из решения и продукта.
        """
        # Проверяем немедленный отказ
        if self.immediate_rejection():
            return REJECTED_STR, None
        user_score = self.scoring_process()
        # Проверка доступности продуктов по скорингу
        available_product = self.check_products_with_score(
            products=self.products,
            user_score=user_score,
        )
        if available_product is not None:
            return ACCEPTED_STR, available_product
        return REJECTED_STR, None


class ScoringPioneer(ScoringBase):
    """Класс скоринга первичника."""
    available_products_with_score = get_available_pioneer_products_with_score()
    min_score_for_acceptance = MIN_PIONEER_SCORE_FOR_PRODUCT

    def immediate_rejection(self) -> Any:
        """Возвращает True, если антифрод первичника выдает немедленный отказ."""
        payload = {
            'user_data': self.user_data.model_dump()
        }
        response = self.antifraud_service_client.check_pioneer(payload)
        return response['decision'] == 'rejected'


class ScoringRepeater(ScoringBase):
    """Класс скоринга повторника."""
    available_products_with_score = get_available_repeater_products_with_score()
    min_score_for_acceptance = MIN_REPEATER_SCORE_FOR_PRODUCT

    def immediate_rejection(self) -> Any:
        """Возвращает True, если антифрод повторника выдает немедленный отказ."""
        user_data = self.user_data.model_dump()
        phone = user_data.pop('phone')

        payload = {
            'phone': phone,
            'current_profile': user_data,
        }

        response = self.antifraud_service_client.check_repeater(payload)
        return response['decision'] == 'rejected'


def generate_loan_id(phone: str) -> str:
    """Генерирует уникальный loan_id в формате loan_{phone}_{timestamp}."""
    timestamp = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
    return f'loan_{phone}_{timestamp}'
