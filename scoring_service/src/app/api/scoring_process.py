from common.schemas.product import ProductRead

from app.constants import (
    ADULT_AGE,
    AVERAGE_AGE,
    AVERAGE_INCOME,
    FREELANCE_STR,
    HIGH_INCOME,
    LOW_INCOME,
    OLD_AGE,
    UNEMPLOYED_STR,
)
from app.schemas.scoring import (
    ProductWrite,
    ScoringUserDataWrite,
)


def check_user_for_immediate_rejection(user_data: ScoringUserDataWrite) -> bool:
    """Функция проверки пользователя на немедленный отказ."""
    return (
            user_data.age < ADULT_AGE
            or user_data.monthly_income < LOW_INCOME
            or user_data.employment_type == UNEMPLOYED_STR
    )


def score_age(age: int) -> int:
    """Функция скоринга возраста."""
    if age <= AVERAGE_AGE:
        score = 1
    elif age <= OLD_AGE:
        score = 3
    else:
        score = 2
    return score


def score_monthly_income(monthly_income: int) -> int:
    """Функция скоринга ежемесячного дохода."""
    if monthly_income < AVERAGE_INCOME:
        score = 1
    elif monthly_income < HIGH_INCOME:
        score = 2
    else:
        score = 3
    return score


def score_employment_type(employment_type: str) -> int:
    """Функция скоринга типа занятости."""
    return 1 if employment_type == FREELANCE_STR else 3


def score_property(has_property: bool) -> int:
    """Функция скоринга недвижимостю"""
    return 2 if has_property else 0


def scoring_process(user_data: ScoringUserDataWrite) -> int:
    """Функция скоринга пользователя."""
    age = user_data.age
    monthly_income = user_data.monthly_income
    employment_type = user_data.employment_type
    score = 0
    score += score_age(age)
    score += score_monthly_income(monthly_income)
    score += score_employment_type(employment_type)
    score += score_property(user_data.has_property)
    return score


def score_product(product_name: str) -> int:
    """Функция оценки продукта."""
    if product_name == 'MicroLoan':
        score = 5
    elif product_name == 'QuickMoney':
        score = 7
    else:
        score = 9
    return score


def check_products_with_score(
        products: list[ProductWrite],
        user_score: int
) -> ProductRead | None:
    """Функция проверки доступности продуктов с учётом скоринга."""
    if user_score < 5:
        return None
    current_product = None
    # Для каждого продукта в списке...
    for new_product in products:
        # Вычисляем его оценку
        product_score = score_product(new_product.name)
        # Если пользователю хватает баллов...
        if user_score >= product_score:
            # и если его текущий продукт лучше...
            if (
                    current_product is not None
                    and score_product(current_product.name) >= product_score
            ):
                # переходим на следующую итерацию...
                continue
            # иначе предлагаем новый продукт
            current_product = new_product
    return current_product
