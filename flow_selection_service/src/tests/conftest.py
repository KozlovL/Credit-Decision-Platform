import pytest
from common.constants import (
    PIONEER_PHONE_NUMBER, REPEATER_PHONE_NUMBER,
    PHONE_JSON_FIELD_NAME,
)
from fastapi.testclient import TestClient

from app.service import app


@pytest.fixture
def client():
    """Фикстура клиента для интеграционных тестов."""
    return TestClient(app)


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
