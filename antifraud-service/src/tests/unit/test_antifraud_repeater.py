import pytest
from datetime import datetime, timedelta, UTC
from common.constants import EmploymentType, CreditStatus
from common.schemas.user import CreditHistoryRead
from app.logic.antifraud import AntifraudRepeater

@pytest.mark.asyncio
async def test_repeater_overdue_loan(mock_previous_profile, credit_history_overdue):
    """Тест на наличие просроченного кредита."""
    current_profile = mock_previous_profile
    repeater = AntifraudRepeater(
        current_profile=current_profile,
        previous_profile=current_profile,
        credit_history=credit_history_overdue,
        phone='79998887777'
    )

    decision, reasons = await repeater.run_checks()
    assert decision == 'rejected'
    assert any('Account has overdue payments' in r for r in reasons)


@pytest.mark.asyncio
async def test_repeater_significant_income_increase(mock_previous_profile, credit_history_recent):
    """Тест на сильное увеличение дохода (+300%)."""
    current_profile = mock_previous_profile.model_copy(update={'monthly_income': 150_000_00})
    repeater = AntifraudRepeater(
        current_profile=current_profile,
        previous_profile=mock_previous_profile,
        credit_history=credit_history_recent,
        phone='79998887777'
    )

    decision, reasons = await repeater.run_checks()
    assert decision == 'rejected'
    assert any('Significant income change detected' in r for r in reasons)


@pytest.mark.asyncio
async def test_repeater_significant_income_decrease(mock_previous_profile, credit_history_recent):
    """Тест на сильное уменьшение дохода (-100%)."""
    current_profile = mock_previous_profile.model_copy(update={'monthly_income': 25_000_00})
    repeater = AntifraudRepeater(
        current_profile=current_profile,
        previous_profile=mock_previous_profile,
        credit_history=credit_history_recent,
        phone='79998887777'
    )

    decision, reasons = await repeater.run_checks()
    assert decision == 'rejected'
    assert any('Significant income change detected' in r for r in reasons)


@pytest.mark.asyncio
async def test_repeater_employment_change_not_allowed(mock_previous_profile, credit_history_recent):
    """Тест на изменение типа трудоустройства."""
    current_profile = mock_previous_profile.model_copy(update={'employment_type': EmploymentType.FREELANCE})
    repeater = AntifraudRepeater(
        current_profile=current_profile,
        previous_profile=mock_previous_profile,
        credit_history=credit_history_recent,
        phone='79998887777'
    )

    decision, reasons = await repeater.run_checks()
    assert decision == 'rejected'
    assert any('Employment type changed from full_time' in r for r in reasons)


@pytest.mark.asyncio
async def test_repeater_passed(mock_previous_profile, credit_history_recent):
    """Тест на валидную проверку антифрода."""
    repeater = AntifraudRepeater(
        current_profile=mock_previous_profile,
        previous_profile=mock_previous_profile,
        credit_history=credit_history_recent,
        phone='79998887777'
    )

    decision, reasons = await repeater.run_checks()
    assert decision == 'passed'
    assert reasons == []


@pytest.mark.asyncio
async def test_repeater_multiple_rules(mock_previous_profile):
    """
    Тест на одновременное срабатывание нескольких правил Repeater:
    - просроченный кредит
    - резко уменьшился доход
    """
    previous_profile = mock_previous_profile
    # Устанавливаем доход ниже минимального
    current_profile = previous_profile.model_copy(update={'monthly_income': previous_profile.monthly_income / 2 - 1})

    credit_history = [
        CreditHistoryRead(
            loan_id='loan_72222222222_20251103123000',
            product_name='MicroLoan',
            amount=100_000,
            issue_date=(datetime.now(UTC).date()),
            term_days=90,
            status=CreditStatus.OVERDUE,
            close_date=None
        )
    ]

    repeater = AntifraudRepeater(
        current_profile=current_profile,
        previous_profile=previous_profile,
        credit_history=credit_history,
        phone='79998887777'
    )

    decision, reasons = await repeater.run_checks()

    assert decision == 'rejected'
    assert any('Account has overdue payments' in r for r in reasons)
    assert any('Significant income change detected' in r for r in reasons)
    assert len(reasons) == 2
