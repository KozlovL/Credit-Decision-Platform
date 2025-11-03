from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio
from common.constants import EmploymentType
from fastapi import FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient

from app.api.routers import main_router
from app.clients.data_service_client import (DataServiceClient,
                                             get_data_service_client)
from app.constants import (ADVANTAGE_PLUS_STR, CONSUMER_LOAN_STR,
                           LOYALTY_LOAN_STR, MICROLOAN_STR, PRIME_CREDIT_STR,
                           QUICK_MONEY_STR)


@pytest.fixture
def valid_repeater_products():
    """Валидные продукты для повторников."""
    return [
        {'name': LOYALTY_LOAN_STR, 'max_amount': 10_000_000, 'term_days': 30, 'interest_rate_daily': 2.0},
        {'name': ADVANTAGE_PLUS_STR, 'max_amount': 25_000_000, 'term_days': 60, 'interest_rate_daily': 1.8},
        {'name': PRIME_CREDIT_STR, 'max_amount': 100_000_000, 'term_days': 120, 'interest_rate_daily': 1.3},
    ]


@pytest.fixture
def user_db(underage_user, user_with_debt, loyalty_user, advantage_user, prime_user, low_score_user):
    """Словарь всех пользователей по телефону."""
    return {
        underage_user['phone']: underage_user,
        user_with_debt['phone']: user_with_debt,
        loyalty_user['phone']: loyalty_user,
        advantage_user['phone']: advantage_user,
        prime_user['phone']: prime_user,
        low_score_user['phone']: low_score_user,
    }


@pytest.fixture
def mock_data_service_client(user_db):
    """
    Мок DataServiceClient, который ищет пользователей в "user_db".
    """
    client = Mock(spec=DataServiceClient)

    def get_user_data(phone: str):
        if phone not in user_db:
            raise HTTPException(status_code=404, detail='not found')
        return user_db[phone]

    client.get_user_data.side_effect = get_user_data
    return client


@pytest_asyncio.fixture
async def app_with_mocked_kafka(mock_data_service_client):
    app = FastAPI()
    app.include_router(main_router)

    # Заменяем Depends внутри эндпоинта
    app.dependency_overrides[get_data_service_client] = lambda: mock_data_service_client

    # Мокаем продюсер
    mock_producer = AsyncMock()
    app.state.producer = mock_producer

    yield app


@pytest_asyncio.fixture
async def client(app_with_mocked_kafka):
    transport = ASGITransport(app=app_with_mocked_kafka)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


@pytest.fixture
def underage_user():
    return {
        'phone': '77777777777',
        'profile': {
            'age': 17,
            'monthly_income': 3_000_000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': False,
        },
        'history': [],
    }

@pytest.fixture
def user_with_debt():
    return {
        'phone': '78888888888',
        'profile': {
            'age': 35,
            'monthly_income': 6_000_000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': True,
        },
        'history': [
            {
                'loan_id': 'loan_78888888888_20240115120000',
                'product_name': QUICK_MONEY_STR,
                'amount': 7_000_000,
                'issue_date': '2024-04-01',
                'term_days': 15,
                'status': 'open',
                'close_date': None,
            }
        ],
    }

@pytest.fixture
def loyalty_user():
    return {
        'phone': '79999990001',
        'profile': {
            'age': 24,
            'monthly_income': 2_000_000,
            'employment_type': EmploymentType.FREELANCE,
            'has_property': True,
        },
        'history': [
            {
                'loan_id': 'loan_79999990001_20240115120000',
                'product_name': MICROLOAN_STR,
                'amount': 4_000_000,
                'issue_date': '2025-05-01',
                'term_days': 30,
                'status': 'closed',
                'close_date': '2025-05-31',
            }
        ],
    }

@pytest.fixture
def advantage_user():
    return {
        'phone': '79999990002',
        'profile': {
            'age': 32,
            'monthly_income': 3_500_000,
            'employment_type': EmploymentType.FREELANCE,
            'has_property': False,
        },
        'history': [
            {
                'loan_id': 'loan_79999990002_20240115120000',
                'product_name': QUICK_MONEY_STR,
                'amount': 7_000_000,
                'issue_date': '2025-07-01',
                'term_days': 15,
                'status': 'closed',
                'close_date': '2025-07-16',
            }
        ],
    }

@pytest.fixture
def prime_user():
    return {
        'phone': '79999990003',
        'profile': {
            'age': 40,
            'monthly_income': 10_000_000,
            'employment_type': EmploymentType.FULL_TIME,
            'has_property': True,
        },
        'history': [
            {
                'loan_id': 'loan_79999990003_20220115120000',
                'product_name': CONSUMER_LOAN_STR,
                'amount': 5_000_000,
                'issue_date': '2022-01-15',
                'term_days': 90,
                'status': 'closed',
                'close_date': '2022-06-01',
            }
        ],
    }

@pytest.fixture
def low_score_user():
    return {
        'phone': '79999990004',
        'profile': {
            'age': 23,
            'monthly_income': 20_000,
            'employment_type': EmploymentType.FREELANCE,
            'has_property': False,
        },
        'history': [
            {
                'loan_id': 'loan_79999990004_20241015120000',
                'product_name': MICROLOAN_STR,
                'amount': 30_000,
                'issue_date': '2025-04-15',
                'term_days': 30,
                'status': 'closed',
                'close_date': '2025-05-15',
            }
        ],
    }


@pytest.fixture
def repeater_not_adult_payload(underage_user, valid_repeater_products):
    return {
        'phone': underage_user['phone'],
        'products': valid_repeater_products
    }

@pytest.fixture
def repeater_with_debt_payload(user_with_debt, valid_repeater_products):
    return {
        'phone': user_with_debt['phone'],
        'products': valid_repeater_products
    }

@pytest.fixture
def repeater_loyalty_payload(loyalty_user, valid_repeater_products):
    return {
        'phone': loyalty_user['phone'],
        'products': valid_repeater_products
    }

@pytest.fixture
def repeater_advantage_payload(advantage_user, valid_repeater_products):
    return {
        'phone': advantage_user['phone'],
        'products': valid_repeater_products
    }

@pytest.fixture
def repeater_prime_payload(prime_user, valid_repeater_products):
    return {
        'phone': prime_user['phone'],
        'products': valid_repeater_products
    }

@pytest.fixture
def repeater_low_score_payload(low_score_user, valid_repeater_products):
    return {
        'phone': low_score_user['phone'],
        'products': valid_repeater_products
    }

@pytest.fixture
def invalid_product_payload(loyalty_user):
    invalid_product = {
        'name': 'InvalidProduct',
        'max_amount': 1_000_000,
        'term_days': 30,
        'interest_rate_daily': 2.0
    }
    return {
        'phone': loyalty_user['phone'],
        'products': [invalid_product]
    }
