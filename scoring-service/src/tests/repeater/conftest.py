from datetime import date, timedelta

import pytest
from common.constants import EmploymentType
from starlette.testclient import TestClient

from app.constants import (
    LOYALTY_LOAN_STR, ADVANTAGE_PLUS_STR, PRIME_CREDIT_STR,
    MICROLOAN_STR, QUICK_MONEY_STR, CONSUMER_LOAN_STR,
)
from app.service import app


@pytest.fixture(scope='session')
def client():
    """Тестовый клиент FastAPI."""
    return TestClient(app)


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
    phone = '79999999999'
    profile = {
        'age': 30,
        'monthly_income': 5000000,
        'employment_type': EmploymentType.FULL_TIME,
        'has_property': True,
    }
    history = [
        {
            'loan_id': f'loan_{phone}_20240115120000',
            'product_name': MICROLOAN_STR,
            'amount': 5000000,
            'issue_date': '2024-01-15',
            'term_days': 30,
            'status': 'closed',
            'close_date': '2024-02-15',
        }
    ]
    return {'phone': phone, 'profile': profile, 'history': history}


@pytest.fixture
def existing_underage_user():
    """Пользователь младше 18 лет."""
    phone = '77777777777'
    profile = {
        'age': 17,
        'monthly_income': 3000000,
        'employment_type': EmploymentType.FULL_TIME,
        'has_property': False,
    }
    return {'phone': phone, 'profile': profile, 'history': []}


@pytest.fixture
def existing_user_with_debt():
    """Пользователь с открытым кредитом."""
    phone = '78888888888'
    profile = {
        'age': 35,
        'monthly_income': 6000000,
        'employment_type': EmploymentType.FULL_TIME,
        'has_property': True,
    }
    history = [
        {
            'loan_id': f'loan_{phone}_20240115120000',
            'product_name': QUICK_MONEY_STR,
            'amount': 7000000,
            'issue_date': (date.today() - timedelta(days=400)).isoformat(),
            'term_days': 15,
            'status': 'open',
            'close_date': None,
        }
    ]
    return {'phone': phone, 'profile': profile, 'history': history}


@pytest.fixture
def existing_user_loyalty():
    phone = '79999990001'
    profile = {
        'age': 24,               # +1
        'monthly_income': 2000000,  # +1
        'employment_type': EmploymentType.FREELANCE,  # +1
        'has_property': True,   # +2
    }
    history = [
        {
            'loan_id': f'loan_{phone}_20240115120000',
            'product_name': MICROLOAN_STR,
            'amount': 4000000,  # <50_000 -> +1
            'issue_date': '2025-05-01',  # <1 год назад -> +0
            'term_days': 30,
            'status': 'closed',
            'close_date': '2025-05-31',
        }
    ]
    return {'phone': phone, 'profile': profile, 'history': history}


@pytest.fixture
def existing_user_advantage():
    phone = '79999990002'
    profile = {
        'age': 32,                 # +3
        'monthly_income': 3500000,   # +2
        'employment_type': EmploymentType.FREELANCE,  # +1
        'has_property': False,       # +0
    }
    history = [
        {
            'loan_id': f'loan_{phone}_20240115120000',
            'product_name': QUICK_MONEY_STR,
            'amount': 7000000,       # 50_000–100_000 -> +2
            'issue_date': '2025-07-01',  # <1 год назад -> +0
            'term_days': 15,
            'status': 'closed',
            'close_date': '2025-07-16',
        }
    ]
    return {'phone': phone, 'profile': profile, 'history': history}


@pytest.fixture
def existing_user_prime():
    """Пользователь с суммарным скором ≥10 для PrimeCredit."""
    phone = '79999990003'
    profile = {
        'age': 40,
        'monthly_income': 10000000,
        'employment_type': EmploymentType.FULL_TIME,
        'has_property': True,
    }
    history = [
        {
            'loan_id': f'loan_{phone}_20220115120000',
            'product_name': CONSUMER_LOAN_STR,
            'amount': 5000000,
            'issue_date': '2022-01-15',
            'term_days': 90,
            'status': 'closed',
            'close_date': '2022-06-01',
        }
    ]
    return {'phone': phone, 'profile': profile, 'history': history}


@pytest.fixture
def existing_user_with_very_low_score():
    """Пользователь с суммарным скором <6 (отказ)."""
    phone = '79999990004'
    profile = {
        'age': 23,  # +1
        'monthly_income': 20000,  # +1
        'employment_type': EmploymentType.FREELANCE,  # +1
        'has_property': False,  # +0
    }
    history = [
        {
            'loan_id': f'loan_{phone}_20241015120000',
            'product_name': MICROLOAN_STR,
            'amount': 30000,  # < 50 000 -> +1
            'issue_date': '2025-04-15',  # < 1 года назад -> +0
            'term_days': 30,
            'status': 'closed',
            'close_date': '2025-05-15',
        }
    ]
    return {'phone': phone, 'profile': profile, 'history': history}


@pytest.fixture
def existing_user_payload(valid_repeater_products):
    """Пользователь, которого нет в базе (используется для 404)."""
    return {
        'phone': '79999990099',
        'products': valid_repeater_products,
    }


@pytest.fixture
def invalid_product_payload(existing_user):
    """Payload с несуществующим продуктом."""
    return {
        'phone': existing_user['phone'],
        'products': [
            {
                'name': 'InvalidProduct',
                'max_amount': 1000000,
                'term_days': 30,
                'interest_rate_daily': 2.0
            }
        ],
    }


@pytest.fixture
def repeater_with_debt_payload(
        existing_user_with_debt,
        valid_repeater_products
):
    """Payload для повторника с долгом."""
    return {
        'phone': existing_user_with_debt['phone'],
        'products': valid_repeater_products,
    }


@pytest.fixture
def not_adult_payload(existing_underage_user, valid_repeater_products):
    """Payload для несовершеннолетнего пользователя."""
    return {
        'phone': existing_underage_user['phone'],
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_loyaltyloan_payload(
        existing_user_loyalty,
        valid_repeater_products
):
    return {
        'phone': existing_user_loyalty['phone'],
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_advantage_payload(
        existing_user_advantage,
        valid_repeater_products
):
    return {
        'phone': existing_user_advantage['phone'],
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_prime_payload(existing_user_prime, valid_repeater_products):
    return {
        'phone': existing_user_prime['phone'],
        'products': valid_repeater_products,
    }


@pytest.fixture
def repeater_low_score_payload(
        existing_user_with_very_low_score,
        valid_repeater_products
):
    return {
        'phone': existing_user_with_very_low_score['phone'],
        'products': valid_repeater_products,
    }
