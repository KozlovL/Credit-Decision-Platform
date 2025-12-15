from http import HTTPStatus
import pytest
from app.constants import (
    REPEATER_SCORING_URL, ACCEPTED_STR, REJECTED_STR,
    LOYALTY_LOAN_STR, ADVANTAGE_PLUS_STR, PRIME_CREDIT_STR
)

@pytest.mark.asyncio
async def test_rejects_if_user_not_exists(client, valid_repeater_products):
    """Новый пользователь: 404 из user-data-service => обработка как нового пользователя"""
    payload = {
        'phone': '70000000000',  # несуществующий телефон
        'products': valid_repeater_products
    }
    response = await client.post(REPEATER_SCORING_URL, json=payload)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_rejects_if_product_not_exists(client, invalid_product_payload):
    """Ошибка 400, если продукт не существует"""
    response = await client.post(REPEATER_SCORING_URL, json=invalid_product_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_immediate_rejection_due_to_age(client, repeater_not_adult_payload, mock_antifraud_service_client):
    """Немедленный отказ из-за возраста < 18"""
    mock_antifraud_service_client.check_repeater.return_value = {
        'decision': 'rejected', 'reasons': ['age below minimum']
    }

    response = await client.post(REPEATER_SCORING_URL, json=repeater_not_adult_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_immediate_rejection_due_to_open_debt(client, repeater_with_debt_payload, mock_antifraud_service_client):
    """Немедленный отказ из-за открытого кредита"""
    mock_antifraud_service_client.check_repeater.return_value = {
        'decision': 'rejected', 'reasons': ['has open debt']
    }

    response = await client.post(REPEATER_SCORING_URL, json=repeater_with_debt_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_user_qualifies_for_loyaltyloan(client, repeater_loyalty_payload):
    """Пользователь набирает 6–7 баллов и получает LoyaltyLoan"""

    response = await client.post(REPEATER_SCORING_URL, json=repeater_loyalty_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == LOYALTY_LOAN_STR


@pytest.mark.asyncio
async def test_user_qualifies_for_advantageplus(client, repeater_advantage_payload):
    """Пользователь набирает 8–9 баллов и получает AdvantagePlus"""

    response = await client.post(REPEATER_SCORING_URL, json=repeater_advantage_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == ADVANTAGE_PLUS_STR


@pytest.mark.asyncio
async def test_user_qualifies_for_primecredit(client, repeater_prime_payload):
    """Пользователь набирает ≥10 баллов и получает PrimeCredit"""
    response = await client.post(REPEATER_SCORING_URL, json=repeater_prime_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == PRIME_CREDIT_STR


@pytest.mark.asyncio
async def test_user_rejected_due_to_low_score(client, repeater_low_score_payload):
    """Пользователь набирает <6 баллов — отказ без продукта"""
    response = await client.post(REPEATER_SCORING_URL, json=repeater_low_score_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None
