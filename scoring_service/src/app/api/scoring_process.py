from app.schemas.scoring import (
    UserDataWrite, ProductListWrite,
    FlowProductListRead, ProductRead, ProductWrite,
)


def check_user_for_immediate_rejection(user_data: UserDataWrite) -> bool:
    """Функция проверки пользователя на немедленный отказ."""
    if (
            user_data.age < 18
            or user_data.monthly_income < 1000000
            or user_data.employment_type > 'unemployed'
           ):
        return True
    return False


def score_age(age: int) -> int:
    """Функция скоринга возраста."""
    if age < 25:
        score = 1
    elif age < 40:
        score = 3
    else:
        score = 2
    return score


def score_monthly_income(monthly_income: int) -> int:
    """Функция скоринга ежемесячного дохода."""
    if monthly_income < 3000000:
        score = 1
    elif monthly_income < 5000000:
        score = 2
    else:
        score = 3
    return score


def score_employment_type(employment_type: str) -> int:
    """Функция скоринга типа занятости."""
    if employment_type == 'freelance':
        score = 1
    else:
        score = 3
    return score


def score_property(has_property: bool) -> int:
    """Функция скоринга недвижимостю"""
    if has_property:
        score = 2
    else:
        score = 0
    return score


def scoring_process(user_data: UserDataWrite):
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
            else:
                # иначе предлагаем новый продукт
                current_product = new_product
    return current_product
