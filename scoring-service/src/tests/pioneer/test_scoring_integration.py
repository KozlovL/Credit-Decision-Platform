from http import HTTPStatus

import respx

from app.constants import (
    ACCEPTED_STR, REJECTED_STR, PIONEER_SCORING_URL, MICROLOAN_STR,
    QUICK_MONEY_STR, CONSUMER_LOAN_STR, DATA_SERVICE_BASE_URL,
)


def test_successful_scoring_accepts_user(client, valid_payload):
    """Пользователь проходит скоринг и получает предложение."""
    phone = valid_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        # Мокаем 404, т.к. пользователь - первичник
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.NOT_FOUND
        )

        # Мокаем создание пользователя
        mock.put('/api/user-data').respond(
            status_code=HTTPStatus.CREATED,
            json={}
        )

        response = client.post(PIONEER_SCORING_URL, json=valid_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product'] is not None


def test_rejects_if_user_already_exists(client, valid_payload):
    """Ошибка 400, если пользователь уже есть в data-service."""
    phone = valid_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(f'/api/user-data?phone={phone}').respond(
            status_code=HTTPStatus.OK,
            json={'phone': phone, 'profile': {}, 'history': []},
        )

        response = client.post(PIONEER_SCORING_URL, json=valid_payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_rejects_if_product_not_exists(client, invalid_product_payload):
    """Ошибка 400, если продукт не существует."""
    phone = invalid_product_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        response = client.post(
            PIONEER_SCORING_URL,
            json=invalid_product_payload
        )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_immediate_rejection_due_to_age(client, underage_payload):
    """Немедленный отказ из-за возраста."""
    phone = underage_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        response = client.post(PIONEER_SCORING_URL, json=underage_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


def test_immediate_rejection_due_to_low_income(client, low_income_payload):
    """Немедленный отказ из-за низкого дохода."""
    phone = low_income_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        response = client.post(PIONEER_SCORING_URL, json=low_income_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


def test_rejection_due_to_unemployed_status(client, unemployed_payload):
    """Немедленный отказ из-за безработного статуса."""
    phone = unemployed_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        response = client.post(PIONEER_SCORING_URL, json=unemployed_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


def test_user_qualifies_for_microloan(client, microloan_payload):
    """Пользователь набирает 5–6 баллов и получает MicroLoan."""
    phone = microloan_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)
        mock.put('/api/user-data').respond(
            status_code=HTTPStatus.CREATED,
            json={}
        )

        response = client.post(PIONEER_SCORING_URL, json=microloan_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == MICROLOAN_STR


def test_user_qualifies_for_quickmoney(client, quickmoney_payload):
    """Пользователь набирает 7–8 баллов и получает QuickMoney."""
    phone = quickmoney_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        mock.put('/api/user-data').respond(
            status_code=HTTPStatus.CREATED,
            json={}
        )

        response = client.post(PIONEER_SCORING_URL, json=quickmoney_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == QUICK_MONEY_STR


def test_user_qualifies_for_consumerloan(client, consumerloan_payload):
    """Пользователь набирает 9 баллов и получает ConsumerLoan."""
    phone = consumerloan_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)
        mock.put('/api/user-data').respond(
            status_code=HTTPStatus.CREATED,
            json={}
        )

        response = client.post(PIONEER_SCORING_URL, json=consumerloan_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == ACCEPTED_STR
    assert data['product']['name'] == CONSUMER_LOAN_STR


def test_user_rejected_due_to_low_score(client, low_score_payload):
    """Пользователь набирает <5 баллов — отказ без продукта."""
    phone = low_score_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        response = client.post(PIONEER_SCORING_URL, json=low_score_payload)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['decision'] == REJECTED_STR
    assert data['product'] is None


def test_raises_502_when_data_service_fails_on_save(client, valid_payload):
    """502, если сервис данных не смог сохранить профиль."""
    phone = valid_payload['user_data']['phone']

    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        mock.get(
            f'/api/user-data?phone={phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        mock.put('/api/user-data').respond(
            status_code=HTTPStatus.BAD_GATEWAY,
        )

        response = client.post(PIONEER_SCORING_URL, json=valid_payload)

    assert response.status_code == HTTPStatus.BAD_GATEWAY
