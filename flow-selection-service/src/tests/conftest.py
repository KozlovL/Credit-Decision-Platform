from unittest.mock import MagicMock, patch, AsyncMock

import pytest
from common.constants import (
    PIONEER_PHONE_NUMBER, REPEATER_PHONE_NUMBER,
    PHONE_JSON_FIELD_NAME,
)
from fastapi.testclient import TestClient

from app.clients.data_service_client import DataServiceClient
from app.service import app


@pytest.fixture(autouse=True)
def mock_redis_dependency(monkeypatch):
    """Подменяем Redis-клиент на мок, чтобы не было подключения к реальному Redis."""
    mock_redis = MagicMock()
    mock_redis.get_from_cache.return_value = None
    monkeypatch.setattr('app.clients.redis_client.get_redis_client', lambda: mock_redis)
    return mock_redis


@pytest.fixture
def client():
    """Фикстура клиента для интеграционных тестов."""
    return TestClient(app)


@pytest.fixture
def mock_redis_client():
    return MagicMock()


@pytest.fixture
def mock_data_client():
    return MagicMock()

@pytest.fixture
def pioneer_phone():
    """Фикстура номера телефона нового пользователя."""
    return PIONEER_PHONE_NUMBER


@pytest.fixture
def repeater_phone():
    """Фикстура номера телефона повторного пользователя."""
    return REPEATER_PHONE_NUMBER


@pytest.fixture
def phone_payload():
    """Фикстура данных схемы для записи при запросе к API."""
    def payload(phone):
        return {PHONE_JSON_FIELD_NAME: phone}
    return payload

@pytest.fixture
def pioneer_products():
    """Фикстура: список продуктов для первичника."""
    return [
        {
            'name': 'MicroLoan',
            'max_amount': 3_000_000,
            'term_days': 30,
            'interest_rate_daily': 2.0,
        },
        {
            'name': 'QuickMoney',
            'max_amount': 1_500_000,
            'term_days': 15,
            'interest_rate_daily': 2.5,
        },
        {
            'name': 'ConsumerLoan',
            'max_amount': 50_000_000,
            'term_days': 90,
            'interest_rate_daily': 1.5,
        },
    ]


@pytest.fixture
def repeater_products():
    """Фикстура: список продуктов для повторника."""
    return [
        {
            'name': 'LoyaltyLoan',
            'max_amount': 5_000_000,
            'term_days': 60,
            'interest_rate_daily': 1.8,
        },
        {
            'name': 'AdvantagePlus',
            'max_amount': 12_000_000,
            'term_days': 90,
            'interest_rate_daily': 1.6,
        },
        {
            'name': 'PrimeCredit',
            'max_amount': 50_000_000,
            'term_days': 180,
            'interest_rate_daily': 1.3,
        },
    ]
