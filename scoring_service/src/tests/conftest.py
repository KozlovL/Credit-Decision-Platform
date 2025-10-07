import pytest
from common.constants import PHONE_JSON_FIELD_NAME
from common.repository.product import AVAILABLE_PRODUCT_LIST
from common.repository.user import USERS_PHONES
from starlette.testclient import TestClient

from app.constants import FREELANCE_STR, UNEMPLOYED_STR, FULL_TIME_STR
from app.service import app


@pytest.fixture(scope='session')
def client():
    """Тестовый клиент FastAPI."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_users():
    """Автоматически очищает 'БД' пользователей перед каждым тестом."""
    USERS_PHONES.clear()


@pytest.fixture
def valid_user_data():
    """Корректные данные пользователя."""
    return {
        'phone': '71111111111',
        'age': 30,
        'monthly_income': 100_000 * 100,  # в копейках
        'employment_type': 'full_time',
        'has_property': True,
    }


@pytest.fixture
def valid_products():
    """Список продуктов из 'БД' (валидный)."""
    return AVAILABLE_PRODUCT_LIST.copy()


@pytest.fixture
def invalid_product():
    """Несуществующий продукт."""
    return {
        'name': 'InvalidLoan',
        'max_amount': 999,
        'term_days': 10,
        'interest_rate_daily': '10.0',
    }


@pytest.fixture
def existing_user(valid_user_data):
    """Добавляем пользователя в БД (эмуляция существующего)."""
    USERS_PHONES.append(valid_user_data[PHONE_JSON_FIELD_NAME])
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
    valid_payload['user_data']['age'] = 10
    return valid_payload


@pytest.fixture
def low_income_payload(valid_payload):
    """Payload с пользователем с низким доходом."""
    valid_payload['user_data']['monthly_income'] = 10000
    return valid_payload


@pytest.fixture
def microloan_payload(valid_products):
    return {
        'user_data': {
            'phone': '79999990001',
            'age': 25,
            'monthly_income': 3000000,
            'employment_type': FULL_TIME_STR,
            'has_property': False
        },
        'products': valid_products
    }


@pytest.fixture
def quickmoney_payload(valid_products):
    return {
        'user_data': {
            'phone': '79999990002',
            'age': 25,
            'monthly_income': 4000000,
            'employment_type': FULL_TIME_STR,
            'has_property': True
        },
        'products': valid_products
    }


@pytest.fixture
def consumerloan_payload(valid_products):
    return {
        'user_data': {
            'phone': '79999990003',
            'age': 45,
            'monthly_income': 8000000,
            'employment_type': FULL_TIME_STR,
            'has_property': True
        },
        'products': valid_products
    }


@pytest.fixture
def unemployed_payload(valid_products):
    return {
        'user_data': {
            'phone': '79999990004',
            'age': 30,
            'monthly_income': 2000000,
            'employment_type': UNEMPLOYED_STR,
            'has_property': False
        },
        'products': valid_products
    }


@pytest.fixture
def low_score_payload(valid_products):
    return {
        'user_data': {
            'phone': '79999990005',
            'age': 19,
            'monthly_income': 1500000,
            'employment_type': FREELANCE_STR,
            'has_property': False
        },
        'products': valid_products
    }
