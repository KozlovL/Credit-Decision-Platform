from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch, AsyncMock
from common.schemas.user import ProfileWrite, CreditHistoryRead
import pytest
from common.constants import (
    PIONEER_PHONE_NUMBER, REPEATER_PHONE_NUMBER,
    PHONE_JSON_FIELD_NAME, EmploymentType, CreditStatus
)
from fastapi.testclient import TestClient

from app.clients.data_service_client import DataServiceClient, get_data_service_client
from app.service import app
from app.clients.redis_client import RedisClient, get_redis_client
from app.logic.antifraud import AntifraudPioneer


@pytest.fixture
def mock_redis_client():
    """Мок для async RedisClient."""
    mock = AsyncMock()
    mock.get_events.return_value = []
    mock.add_event_zset.return_value = None
    return mock


@pytest.fixture
def client():
    """Фикстура клиента для интеграционных тестов."""
    return TestClient(app)


@pytest.fixture
def mock_profile():
    return ProfileWrite(
        age=30,
        monthly_income=50_000_00,
        employment_type=EmploymentType.FULL_TIME,
        has_property=False,
    )

@pytest.fixture
def antifraud(mock_redis_client, mock_profile):
    return AntifraudPioneer(
        redis_client=mock_redis_client,
        current_profile=mock_profile,
        phone='79998887766',
    )

@pytest.fixture
def mock_data_service_client():
    """Мок DataServiceClient для Repeater."""
    mock = AsyncMock(spec=DataServiceClient)
    return mock


@pytest.fixture(autouse=True)
def override_dependencies(mock_redis_client, mock_data_service_client):
    """Переопределяем зависимости FastAPI для тестов."""
    app.dependency_overrides[get_redis_client] = lambda: mock_redis_client
    app.dependency_overrides[get_data_service_client] = lambda: mock_data_service_client
    yield
    app.dependency_overrides.clear()


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


@pytest.fixture
def mock_previous_profile():
    """Предыдущий профиль повторника."""
    return ProfileWrite(
        age=30,
        monthly_income=50_000_00,
        employment_type=EmploymentType.FULL_TIME,
        has_property=False,
    )


@pytest.fixture
def credit_history_recent():
    """Кредит, полученный 10 дней назад, без просрочек."""
    return [
        CreditHistoryRead(
            loan_id='loan_72222222222_20251103123000',
            product_name='ConsumerLoan',
            amount=1_000_000,
            issue_date=(datetime.now(UTC).date() - timedelta(days=10)),  # 10 дней назад
            term_days=90,
            status=CreditStatus.OPEN,
            close_date=None
        )
    ]


@pytest.fixture
def credit_history_overdue():
    """Просроченный кредит (>180 дней)."""
    return [
        CreditHistoryRead(
            loan_id='loan_72222222222_20251103123001',
            product_name='MicroLoan',
            amount=100_000,
            issue_date=(datetime.now(UTC).date()),
            term_days=90,
            status=CreditStatus.OVERDUE,
            close_date=None
        )
    ]


