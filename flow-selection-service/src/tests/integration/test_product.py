from http import HTTPStatus

import pytest
import respx
from common.constants import (
    NULL_PHONE_NUMBER, NOT_STR_PHONE_NUMBER,
    INCORRECT_LENGTH_PHONE, INCORRECT_FIRST_SYMBOL_PHONE,
    INCORRECT_SYMBOL_PHONE, EMPTY_PHONE_NUMBER,
)

from app.constants import (
    PIONEER_FLOW_TYPE, REPEATER_FLOW_TYPE,
    AVAILABLE_PRODUCTS_JSON_FIELD_NAME, FLOW_TYPE_JSON_FIELD_NAME,
    API_PRODUCT_PATH, DATA_SERVICE_BASE_URL,
)


def test_select_flow_pioneer(
        client,
        pioneer_phone,
        phone_payload
):
    """Тест выбора флоу первичника."""
    # Мокаем запрос к сервису данных
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        # Возвращаем 404 для первичника
        mock.get(
            f'/api/user-data?phone={pioneer_phone}'
        ).respond(status_code=HTTPStatus.NOT_FOUND)

        response = client.post(
            API_PRODUCT_PATH,
            json=phone_payload(pioneer_phone)
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data[FLOW_TYPE_JSON_FIELD_NAME] == PIONEER_FLOW_TYPE
        assert len(data[AVAILABLE_PRODUCTS_JSON_FIELD_NAME]) > 0


def test_select_flow_repeater(
        client,
        repeater_phone,
        phone_payload
):
    """Тест выбора флоу повторника."""
    # Мокаем запрос к сервису данных
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        # Возвращаем 200 для повторинка
        mock.get(
            f'/api/user-data?phone={repeater_phone}'
        ).respond(
            status_code=HTTPStatus.OK,
            json={'phone': repeater_phone, 'profile': {}, 'history': []}
        )

        response = client.post(
            API_PRODUCT_PATH,
            json=phone_payload(repeater_phone)
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data[FLOW_TYPE_JSON_FIELD_NAME] == REPEATER_FLOW_TYPE
        assert len(data[AVAILABLE_PRODUCTS_JSON_FIELD_NAME]) > 0


@pytest.mark.parametrize('phone, expected_status', [
    (NULL_PHONE_NUMBER, HTTPStatus.UNPROCESSABLE_ENTITY),
    (EMPTY_PHONE_NUMBER, HTTPStatus.UNPROCESSABLE_ENTITY),
    (NOT_STR_PHONE_NUMBER, HTTPStatus.UNPROCESSABLE_ENTITY),
    (INCORRECT_LENGTH_PHONE, HTTPStatus.UNPROCESSABLE_ENTITY),
    (INCORRECT_FIRST_SYMBOL_PHONE, HTTPStatus.UNPROCESSABLE_ENTITY),
    (INCORRECT_SYMBOL_PHONE, HTTPStatus.UNPROCESSABLE_ENTITY),
])
def test_select_flow_invalid_phones(
        client,
        phone,
        expected_status,
        phone_payload
):
    """Тест для некорректных телефонов с корректным статус-кодом."""
    response = client.post(API_PRODUCT_PATH, json=phone_payload(phone))
    assert response.status_code == expected_status
