from http import HTTPStatus
import pytest

from app.constants import (
    PIONEER_SCORING_URL,
    ACCEPTED_STR,
    REJECTED_STR,
    MICROLOAN_STR,
    QUICK_MONEY_STR,
    CONSUMER_LOAN_STR
)


@pytest.mark.asyncio
async def test_successful_scoring_accepts_user(client, valid_payload):
    """Пользователь проходит скоринг и получает предложение."""
    response = await client.post(PIONEER_SCORING_URL, json=valid_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product'] is not None


@pytest.mark.asyncio
async def test_immediate_rejection_due_to_age(client, underage_payload, mock_antifraud_service_client):
    """Немедленный отказ из-за возраста."""
    mock_antifraud_service_client.check_pioneer.return_value = {'decision': 'rejected', 'reasons': ['under minimum age']}

    response = await client.post(PIONEER_SCORING_URL, json=underage_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_immediate_rejection_due_to_low_income(client, low_income_payload, mock_antifraud_service_client):
    """Немедленный отказ из-за низкого дохода."""
    mock_antifraud_service_client.check_pioneer.return_value = {'decision': 'rejected', 'reasons': ['monthly income below threshold']}

    response = await client.post(PIONEER_SCORING_URL, json=low_income_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_rejection_due_to_unemployed_status(client, unemployed_payload, mock_antifraud_service_client):
    """Немедленный отказ из-за безработного статуса."""
    mock_antifraud_service_client.check_pioneer.return_value = {'decision': 'rejected', 'reasons': ['employment type changed from full_time']}

    response = await client.post(PIONEER_SCORING_URL, json=unemployed_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_user_qualifies_for_microloan(client, microloan_payload, mock_antifraud_service_client):
    """Пользователь набирает баллы и получает MicroLoan."""
    mock_antifraud_service_client.check_pioneer.return_value = {'decision': 'passed', 'reasons': []}

    response = await client.post(PIONEER_SCORING_URL, json=microloan_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == MICROLOAN_STR


@pytest.mark.asyncio
async def test_user_qualifies_for_quickmoney(client, quickmoney_payload, mock_antifraud_service_client):
    """Пользователь набирает баллы и получает QuickMoney."""
    mock_antifraud_service_client.check_pioneer.return_value = {'decision': 'passed', 'reasons': []}

    response = await client.post(PIONEER_SCORING_URL, json=quickmoney_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == QUICK_MONEY_STR


@pytest.mark.asyncio
async def test_user_qualifies_for_consumerloan(client, consumerloan_payload, mock_antifraud_service_client):
    """Пользователь набирает баллы и получает ConsumerLoan."""
    mock_antifraud_service_client.check_pioneer.return_value = {'decision': 'passed', 'reasons': []}

    response = await client.post(PIONEER_SCORING_URL, json=consumerloan_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == CONSUMER_LOAN_STR


@pytest.mark.asyncio
async def test_user_rejected_due_to_low_score(client, low_score_payload, mock_antifraud_service_client):
    """Пользователь набирает <5 баллов — отказ без продукта."""
    mock_antifraud_service_client.check_pioneer.return_value = {'decision': 'rejected', 'reasons': ['score below minimum']}

    response = await client.post(PIONEER_SCORING_URL, json=low_score_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None
