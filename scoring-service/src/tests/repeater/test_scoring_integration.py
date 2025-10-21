from http import HTTPStatus

from app.constants import (
    REPEATER_SCORING_URL, REJECTED_STR, ACCEPTED_STR,
    LOYALTY_LOAN_STR, ADVANTAGE_PLUS_STR, PRIME_CREDIT_STR,
)


def test_rejects_if_user_not_exists(client, non_existing_user_payload):
    """Ошибка 404, если пользователь отсутствует в БД."""
    response = client.post(REPEATER_SCORING_URL, json=non_existing_user_payload)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_rejects_if_product_not_exists(
        client,
        existing_user,
        invalid_product_payload
):
    """Ошибка 400, если продукт не существует."""
    response = client.post(REPEATER_SCORING_URL, json=invalid_product_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_immediate_rejection_due_to_age(
        client,
        existing_underage_user,
        not_adult_payload
):
    """Немедленный отказ из-за возраста < 18."""
    response = client.post(REPEATER_SCORING_URL, json=not_adult_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


def test_immediate_rejection_due_to_open_debt(
        client,
        repeater_with_debt_payload
):
    """Немедленный отказ из-за открытого просроченного кредита."""
    response = client.post(
        REPEATER_SCORING_URL,
        json=repeater_with_debt_payload
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


def test_user_qualifies_for_loyaltyloan(
        client,
        repeater_loyaltyloan_payload
):
    """Пользователь набирает 6–7 баллов и получает LoyaltyLoan."""
    response = client.post(
        REPEATER_SCORING_URL,
        json=repeater_loyaltyloan_payload
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == LOYALTY_LOAN_STR


def test_user_qualifies_for_advantageplus(
        client,
        repeater_advantage_payload
):
    """Пользователь набирает 8–9 баллов и получает AdvantagePlus."""
    response = client.post(
        REPEATER_SCORING_URL,
        json=repeater_advantage_payload
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == ADVANTAGE_PLUS_STR


def test_user_qualifies_for_primecredit(
        client,
        repeater_prime_payload
):
    """Пользователь набирает ≥10 баллов и получает PrimeCredit."""
    response = client.post(REPEATER_SCORING_URL, json=repeater_prime_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == PRIME_CREDIT_STR


def test_user_rejected_due_to_low_score(
        client,
        repeater_low_score_payload
):
    """Пользователь набирает <6 баллов — отказ без продукта."""
    response = client.post(
        REPEATER_SCORING_URL,
        json=repeater_low_score_payload
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None
