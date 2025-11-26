import pytest
from app.constants import MAX_APPLICATIONS_PER_DAY
from common.constants import EmploymentType, MonthlyIncomeType

@pytest.mark.asyncio
async def test_pioneer_min_age(antifraud, mock_profile):
    """Тест на несовершеннолетие."""
    mock_profile.age = 16
    antifraud.current_profile = mock_profile

    decision, reasons = await antifraud.run_checks()
    assert decision == 'rejected'
    assert any('under minimum age' in r for r in reasons)


@pytest.mark.asyncio
async def test_pioneer_min_income(antifraud, mock_profile):
    """Тест на низкий доход."""
    mock_profile.monthly_income = 500_000
    antifraud.current_profile = mock_profile

    decision, reasons = await antifraud.run_checks()
    assert decision == 'rejected'
    assert any('Monthly income is below minimum threshold' in r for r in reasons)


@pytest.mark.asyncio
async def test_pioneer_unemployed(antifraud, mock_profile):
    """Тест на отсутствие трудоустройства."""
    mock_profile.employment_type = EmploymentType.UNEMPLOYED
    antifraud.current_profile = mock_profile

    decision, reasons = await antifraud.run_checks()
    assert decision == 'rejected'
    assert any('Employment type is not allowed' in r for r in reasons)


@pytest.mark.asyncio
async def test_pioneer_property_low_income(antifraud, mock_profile):
    """Тест на наличие недвижимости при среднем доходе."""
    mock_profile.has_property = True
    mock_profile.monthly_income = MonthlyIncomeType.LOW_INCOME.value
    antifraud.current_profile = mock_profile

    decision, reasons = await antifraud.run_checks()
    assert decision == 'rejected'
    assert any('User has property but income is below threshold' in r for r in reasons)


@pytest.mark.asyncio
async def test_pioneer_daily_application_limit(antifraud, mock_redis_client):
    """Тест на превышение лимита заявок за сутки."""
    mock_redis_client.get_events.return_value = [1] * MAX_APPLICATIONS_PER_DAY
    antifraud.redis = mock_redis_client

    decision, reasons = await antifraud.run_checks()
    assert decision == 'rejected'
    assert any('Daily application limit exceeded' in r for r in reasons)
    mock_redis_client.add_event_zset.assert_awaited_once()


@pytest.mark.asyncio
async def test_pioneer_passed(antifraud, mock_profile, mock_redis_client):
    """Тест валидной проверки антифрода."""
    antifraud.current_profile = mock_profile
    mock_redis_client.get_events.return_value = []
    antifraud.redis = mock_redis_client

    decision, reasons = await antifraud.run_checks()
    assert decision == 'passed'
    assert reasons == []


@pytest.mark.asyncio
async def test_pioneer_multiple_rules(antifraud, mock_profile, mock_redis_client):
    """
    Тест на одновременное срабатывание нескольких правил:
    - возраст меньше минимума
    - доход ниже порога
    - наличие недвижимости при низком доходе
    """
    # Настроим профиль с проблемами
    mock_profile.age = 16  # младше минимального возраста
    mock_profile.monthly_income = MonthlyIncomeType.LOW_INCOME.value - 1  # низкий доход
    mock_profile.has_property = True  # есть недвижимость
    antifraud.current_profile = mock_profile

    # Redis не содержит событий → проверка лимита заявок не срабатывает
    mock_redis_client.get_events.return_value = []
    antifraud.redis = mock_redis_client

    decision, reasons = await antifraud.run_checks()

    assert decision == 'rejected'
    # Проверяем, что все три причины сработали
    assert any('under minimum age' in r for r in reasons)
    assert any('Monthly income is below minimum threshold' in r for r in reasons)
    assert any('User has property but income is below threshold' in r for r in reasons)
    # Количество причин равно 3
    assert len(reasons) == 3
