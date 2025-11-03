from http import HTTPStatus
import pytest
from app.constants import PIONEER_SCORING_URL, ACCEPTED_STR, REJECTED_STR, MICROLOAN_STR, QUICK_MONEY_STR, CONSUMER_LOAN_STR

@pytest.mark.asyncio
async def test_successful_scoring_accepts_user(
    client, valid_payload
):
    """Пользователь проходит скоринг и получает предложение."""
    response = await client.post(PIONEER_SCORING_URL, json=valid_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data['decision'] == ACCEPTED_STR
    assert data['product'] is not None


@pytest.mark.asyncio
async def test_rejects_if_product_not_exists(
    client, invalid_product_payload
):
    """Ошибка 400, если продукт не существует."""
    response = await client.post(PIONEER_SCORING_URL, json=invalid_product_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_immediate_rejection_due_to_age(
    client, underage_payload
):
    """Немедленный отказ из-за возраста."""
    response = await client.post(PIONEER_SCORING_URL, json=underage_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_immediate_rejection_due_to_low_income(
    client, low_income_payload
):
    """Немедленный отказ из-за низкого дохода."""
    response = await client.post(PIONEER_SCORING_URL, json=low_income_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_rejection_due_to_unemployed_status(
    client, unemployed_payload
):
    """Немедленный отказ из-за безработного статуса."""
    response = await client.post(PIONEER_SCORING_URL, json=unemployed_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


@pytest.mark.asyncio
async def test_user_qualifies_for_microloan(
    client, microloan_payload
):
    """Пользователь набирает баллы и получает MicroLoan."""
    response = await client.post(PIONEER_SCORING_URL, json=microloan_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == MICROLOAN_STR


@pytest.mark.asyncio
async def test_user_qualifies_for_quickmoney(
    client, quickmoney_payload
):
    """Пользователь набирает баллы и получает QuickMoney."""
    response = await client.post(PIONEER_SCORING_URL, json=quickmoney_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == QUICK_MONEY_STR


@pytest.mark.asyncio
async def test_user_qualifies_for_consumerloan(
    client, consumerloan_payload
):
    """Пользователь набирает баллы и получает ConsumerLoan."""
    response = await client.post(PIONEER_SCORING_URL, json=consumerloan_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == CONSUMER_LOAN_STR


@pytest.mark.asyncio
async def test_user_rejected_due_to_low_score(
    client, low_score_payload
):
    """Пользователь набирает <5 баллов — отказ без продукта."""
    response = await client.post(PIONEER_SCORING_URL, json=low_score_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None
