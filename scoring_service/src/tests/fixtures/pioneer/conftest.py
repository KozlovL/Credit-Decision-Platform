import pytest
from common.constants import EmploymentType
from common.repository.user import add_user, USERS
from common.schemas.user import UserDataWrite
from starlette.testclient import TestClient

from app.constants import MICROLOAN_STR, QUICK_MONEY_STR, CONSUMER_LOAN_STR
from app.service import app


@pytest.fixture(scope='session')
def client():
    """Тестовый клиент FastAPI."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Очищает БД перед каждым тестом."""
    USERS.clear()


@pytest.fixture
def valid_user_data():
    """Корректные данные пользователя."""
    return {
        'phone': '71111111111',
        'age': 30,
        'monthly_income': 100_000 * 100,
        'employment_type': 'full_time',
        'has_property': True,
    }


@pytest.fixture
def valid_products():
    """Список продуктов из "БД" (валидный, с полными данными)."""
    return [
        {
            'name': MICROLOAN_STR,
            'max_amount': 3_000_000,
            'term_days': 30,
            'interest_rate_daily': 2.0,
        },
        {
            'name': QUICK_MONEY_STR,
            'max_amount': 1_500_000,
            'term_days': 15,
            'interest_rate_daily': 2.5,
        },
        {
            'name': CONSUMER_LOAN_STR,
            'max_amount': 50_000_000,
            'term_days': 90,
            'interest_rate_daily': 1.5,
        }
    ]


@pytest.fixture
def invalid_product():
    """Несуществующий продукт."""
    return {
        'name': 'InvalidLoan',
        'max_amount': 999,
        'term_days': 10,
        'interest_rate_daily': 10.0,
    }


@pytest.fixture
def existing_user(valid_user_data):
    """Добавляем пользователя в БД (эмуляция существующего)."""
    add_user(UserDataWrite(**valid_user_data))
    return valid_user_data


@pytest.fixture
def valid_payload(valid_user_data, valid_products):
    """Полный валидный payload для успешного запроса."""
    return {
        'user_data': valid_user_data,
        'products': valid_products,
    }


@pytest.fixture
def invalid_product_payload(valid_user_data, invalid_product):
    """Payload с несуществующим продуктом."""
    return {
        'user_data': valid_user_data,
        'products': [invalid_product],
    }


@pytest.fixture
def underage_payload(valid_payload):
    """Payload с пользователем младше ADULT_AGE."""
    payload = valid_payload.copy()
    payload['user_data'] = payload['user_data'].copy()
    payload['user_data']['age'] = 10
    return payload


@pytest.fixture
def low_income_payload(valid_payload):
    """Payload с пользователем с низким доходом."""
    payload = valid_payload.copy()
    payload['user_data'] = payload['user_data'].copy()
    payload['user_data']['monthly_income'] = 10_000
    return payload


@pytest.fixture
def microloan_payload(valid_products):
    """Payload для пользователя, который должен получить MicroLoan."""
    return {
        'user_data': {
            'phone': '79999990001',
            'age': 25,
            'monthly_income': 3_000_000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': False
        },
        'products': valid_products
    }


@pytest.fixture
def quickmoney_payload(valid_products):
    """Payload для пользователя, который должен получить QuickMoney."""
    return {
        'user_data': {
            'phone': '79999990002',
            'age': 25,
            'monthly_income': 4_000_000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': True
        },
        'products': valid_products
    }


@pytest.fixture
def consumerloan_payload(valid_products):
    """Payload для пользователя, который должен получить ConsumerLoan."""
    return {
        'user_data': {
            'phone': '79999990003',
            'age': 45,
            'monthly_income': 8_000_000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': True
        },
        'products': valid_products
    }


@pytest.fixture
def unemployed_payload(valid_products):
    """Payload для пользователя с безработным статусом."""
    return {
        'user_data': {
            'phone': '79999990004',
            'age': 30,
            'monthly_income': 2_000_000,
            'employment_type': EmploymentType.UNEMPLOYED,
            'has_property': False
        },
        'products': valid_products
    }


@pytest.fixture
def low_score_payload(valid_products):
    """Payload для пользователя с низкой суммой баллов (<5)."""
    return {
        'user_data': {
            'phone': '79999990005',
            'age': 19,
            'monthly_income': 1_500_000,
            'employment_type': EmploymentType.FREELANCE,
            'has_property': False
        },
        'products': valid_products
    }
