from http import HTTPStatus

import respx

from app.constants import (
    REPEATER_SCORING_URL, REJECTED_STR, ACCEPTED_STR,
    LOYALTY_LOAN_STR, ADVANTAGE_PLUS_STR, PRIME_CREDIT_STR,
    DATA_SERVICE_BASE_URL,
)


def test_rejects_if_user_not_exists(client, existing_user_payload):
    """Ошибка 404, если пользователь отсутствует в БД."""
    phone = existing_user_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        response = client.post(
            REPEATER_SCORING_URL,
            json=existing_user_payload
        )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_rejects_if_product_not_exists(
        client,
        existing_user,
        invalid_product_payload
):
    """Ошибка 400, если продукт не существует."""
    phone = invalid_product_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json=existing_user
        )

        response = client.post(
            REPEATER_SCORING_URL,
            json=invalid_product_payload
        )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_immediate_rejection_due_to_age(
        client,
        existing_underage_user,
        not_adult_payload
):
    """Немедленный отказ из-за возраста < 18."""
    phone = not_adult_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json=existing_underage_user
        )

        response = client.post(REPEATER_SCORING_URL, json=not_adult_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


def test_immediate_rejection_due_to_open_debt(
        client,
        repeater_with_debt_payload,
        existing_user_with_debt
):
    """Немедленный отказ из-за открытого просроченного кредита."""
    phone = repeater_with_debt_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json=existing_user_with_debt
        )

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
        repeater_loyaltyloan_payload,
        existing_user_loyalty
):
    """Пользователь набирает 6–7 баллов и получает LoyaltyLoan."""
    phone = repeater_loyaltyloan_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json=existing_user_loyalty
        )
        mock.put('/api/user-data').respond(status_code=HTTPStatus.OK, json={})

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
        repeater_advantage_payload,
        existing_user_advantage
):
    """Пользователь набирает 8–9 баллов и получает AdvantagePlus."""
    phone = repeater_advantage_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json=existing_user_advantage
        )
        mock.put('/api/user-data').respond(status_code=HTTPStatus.OK, json={})

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
        repeater_prime_payload,
        existing_user_prime
):
    """Пользователь набирает ≥10 баллов и получает PrimeCredit."""
    phone = repeater_prime_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json=existing_user_prime
        )
        mock.put('/api/user-data').respond(status_code=HTTPStatus.OK, json={})

        response = client.post(
            REPEATER_SCORING_URL,
            json=repeater_prime_payload
        )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == PRIME_CREDIT_STR


def test_user_rejected_due_to_low_score(
        client,
        repeater_low_score_payload,
        existing_user_with_very_low_score
):
    """Пользователь набирает <6 баллов — отказ без продукта."""
    phone = repeater_low_score_payload['phone']
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json=existing_user_with_very_low_score
        )

        response = client.post(
            REPEATER_SCORING_URL,
            json=repeater_low_score_payload
        )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None
