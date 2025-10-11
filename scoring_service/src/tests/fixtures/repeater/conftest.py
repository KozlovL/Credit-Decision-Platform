from datetime import date, timedelta

import pytest
from common.constants import EmploymentType
from common.repository.user import USERS, add_user
from common.schemas.product import ProductWrite
from common.schemas.user import UserDataWrite
from starlette.testclient import TestClient

from app.constants import (
    LOYALTY_LOAN_STR, PRIME_CREDIT_STR,
    ADVANTAGE_PLUS_STR, MICROLOAN_STR, QUICK_MONEY_STR, CONSUMER_LOAN_STR,
    AgeType, CreditStatusType,
)
from app.service import app


@pytest.fixture(scope='session')
def client():
    """Тестовый клиент FastAPI."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Очищает USERS между тестами."""
    USERS.clear()
    yield
    USERS.clear()


@pytest.fixture
def valid_repeater_products():
    """Валидные продукты для повторников."""
    return [
        {
            'name': LOYALTY_LOAN_STR,
            'max_amount': 10_000_000,
            'term_days': 30,
            'interest_rate_daily': 2.0
        },
        {
            'name': ADVANTAGE_PLUS_STR,
            'max_amount': 25_000_000,
            'term_days': 60,
            'interest_rate_daily': 1.8
        },
        {
            'name': PRIME_CREDIT_STR,
            'max_amount': 100_000_000,
            'term_days': 120,
            'interest_rate_daily': 1.3
        },
    ]


@pytest.fixture
def existing_user():
    """Пользователь с закрытым кредитом."""
    user_data = UserDataWrite(
        phone='79999999999',
        age=30,
        monthly_income=50_00000,
        employment_type=EmploymentType.FULL_TIME,
        has_property=True,
    )
    user = add_user(user_data)

    product = ProductWrite(
        name=MICROLOAN_STR,
        max_amount=50_00000,
        term_days=30,
        interest_rate_daily=2.0,
    )
    user.add_credit_note(product)
    return user


@pytest.fixture
def non_existing_user_payload(valid_repeater_products):
    """Пользователь отсутствует в БД."""
    return {
        'user_data': {
            'phone': '79999990099',  # уникальный телефон, которого нет в USERS
            'age': 30,
            'monthly_income': 50_00000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': True
        },
        'products': valid_repeater_products
    }


@pytest.fixture
def existing_user_with_debt():
    """Пользователь с открытым кредитом, взятым более 6 месяцев назад."""
    user_data = UserDataWrite(
        phone='78888888888',
        age=35,
        monthly_income=60_00000,
        employment_type=EmploymentType.FULL_TIME,
        has_property=True,
    )
    user = add_user(user_data)

    product = ProductWrite(
        name=QUICK_MONEY_STR,
        max_amount=70_00000,
        term_days=15,
        interest_rate_daily=2.5,
    )
    user.add_credit_note(product)
    # Просроченный кредит
    user.credit_history[-1].status = CreditStatusType.OPEN
    user.credit_history[-1].issue_date = date.today() - timedelta(days=400)
    return user


@pytest.fixture
def existing_underage_user():
    """Пользователь младше 18 лет."""
    user_data = UserDataWrite(
        phone='77777777777',
        age=17,
        monthly_income=30_00000,
        employment_type=EmploymentType.FULL_TIME,
        has_property=False,
    )
    return add_user(user_data)


@pytest.fixture
def existing_user_loyalty():
    """Пользователь с суммарным скором 6–7 для LoyaltyLoan."""
    user_data = UserDataWrite(
        phone='79999990001',
        age=25,
        monthly_income=30_00000,
        employment_type=EmploymentType.FREELANCE,
        has_property=False,
    )
    user = add_user(user_data)

    # Закрытая кредитная история >1 года назад → +3 балла
    product = ProductWrite(
        name='MicroLoan',
        max_amount=500_0000,
        term_days=30,
        interest_rate_daily=2.0,
    )
    user.add_credit_note(product)

    return user


@pytest.fixture
def existing_user_advantage():
    """Пользователь с суммарным скором 8–9 для AdvantagePlus."""
    user_data = UserDataWrite(
        phone='79999990002',
        age=30,
        monthly_income=45_00000,
        employment_type=EmploymentType.FREELANCE,
        has_property=True,
    )
    user = add_user(user_data)

    # Закрытая кредитная история >1 года назад → +3 балла
    product = ProductWrite(
        name=QUICK_MONEY_STR,
        max_amount=70_0000,
        term_days=15,
        interest_rate_daily=2.5,
    )
    user.add_credit_note(product)

    return user


@pytest.fixture
def existing_user_prime():
    """Пользователь с суммарным скором ≥10 для PrimeCredit."""
    user_data = UserDataWrite(
        phone='79999990003',
        age=40,
        monthly_income=100_00000,
        employment_type=EmploymentType.FULL_TIME,
        has_property=True,
    )
    user = add_user(user_data)

    # Закрытая кредитная история >1 года назад → +3 балла
    product = ProductWrite(
        name=CONSUMER_LOAN_STR,
        max_amount=500_0000,
        term_days=90,
        interest_rate_daily=1.5,
    )
    user.add_credit_note(product)

    return user


@pytest.fixture
def existing_user_with_very_low_score():
    """Пользователь с суммарным скором <6."""
    user_data = UserDataWrite(
        phone='79999990004',
        age=80,
        monthly_income=100_0000,
        employment_type=EmploymentType.UNEMPLOYED,
        has_property=False,
    )
    user = add_user(user_data)

    product = ProductWrite(
        name=CONSUMER_LOAN_STR,
        max_amount=500_0000,
        term_days=90,
        interest_rate_daily=1.5,
    )
    user.add_credit_note(product)

    return user


@pytest.fixture
def valid_repeater_payload(valid_repeater_products, existing_user):
    """Корректный запрос для повторника."""
    return {
        'user_data': {
            'phone': existing_user.phone,
            'age': existing_user.age,
            'monthly_income': existing_user.monthly_income,
            'employment_type': existing_user.employment_type,
            'has_property': existing_user.has_property,
        },
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_with_debt_payload(
        valid_repeater_products,
        existing_user_with_debt
):
    """Корректный запрос для повторника."""
    return {
        'user_data': {
            'phone': existing_user_with_debt.phone,
            'age': existing_user_with_debt.age,
            'monthly_income': existing_user_with_debt.monthly_income,
            'employment_type': existing_user_with_debt.employment_type,
            'has_property': existing_user_with_debt.has_property,
        },
        'products': valid_repeater_products,
    }


@pytest.fixture
def not_adult_payload(valid_repeater_products, existing_user):
    """Несовершеннолетний повторник."""
    return {
        'user_data': {
            'phone': existing_user.phone,
            'age': AgeType.ADULT_AGE - 1,
            'monthly_income': existing_user.monthly_income,
            'employment_type': existing_user.employment_type,
            'has_property': existing_user.has_property,
        },
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_low_score_payload(
        existing_user_with_very_low_score,
        valid_repeater_products
):
    """Запрос с низким скором (<6)."""
    return {
        'user_data': {
            'phone': existing_user_with_very_low_score.phone,
            'age': existing_user_with_very_low_score.age,
            'monthly_income': existing_user_with_very_low_score.monthly_income,
            'employment_type': (
                existing_user_with_very_low_score.employment_type
            ),
            'has_property': existing_user_with_very_low_score.has_property,
        },
        'products': valid_repeater_products,
    }


@pytest.fixture
def invalid_product_payload(existing_user):
    """Запрос с несуществующим продуктом."""
    return {
        'user_data': {
            'phone': existing_user.phone,
            'age': existing_user.age,
            'monthly_income': existing_user.monthly_income,
            'employment_type': existing_user.employment_type,
            'has_property': existing_user.has_property,
        },
        'products': [{
            'name': 'InvalidProduct',
            'max_amount': 10_000_00000,
            'term_days': 30,
            'interest_rate_daily': 2.0
        }],
    }


@pytest.fixture
def repeater_loyaltyloan_payload(
        existing_user_loyalty,
        valid_repeater_products
):
    """Payload для пользователя, ожидающего LoyaltyLoan."""
    return {
        'user_data': {
            'phone': existing_user_loyalty.phone,
            'age': existing_user_loyalty.age,
            'monthly_income': existing_user_loyalty.monthly_income,
            'employment_type': existing_user_loyalty.employment_type,
            'has_property': existing_user_loyalty.has_property,
        },
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_advantage_payload(
        existing_user_advantage,
        valid_repeater_products
):
    """Payload для пользователя, ожидающего AdvantagePlus."""
    return {
        'user_data': {
            'phone': existing_user_advantage.phone,
            'age': existing_user_advantage.age,
            'monthly_income': existing_user_advantage.monthly_income,
            'employment_type': existing_user_advantage.employment_type,
            'has_property': existing_user_advantage.has_property,
        },
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_prime_payload(existing_user_prime, valid_repeater_products):
    """Payload для пользователя, ожидающего PrimeCredit."""
    return {
        'user_data': {
            'phone': existing_user_prime.phone,
            'age': existing_user_prime.age,
            'monthly_income': existing_user_prime.monthly_income,
            'employment_type': existing_user_prime.employment_type,
            'has_property': existing_user_prime.has_property,
        },
        'products': valid_repeater_products,
    }
