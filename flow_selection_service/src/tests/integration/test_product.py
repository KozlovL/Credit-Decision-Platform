from http import HTTPStatus

import pytest
from common.constants import (
    NULL_PHONE_NUMBER, NOT_STR_PHONE_NUMBER,
    INCORRECT_LENGTH_PHONE, INCORRECT_FIRST_SYMBOL_PHONE,
    INCORRECT_SYMBOL_PHONE, EMPTY_PHONE_NUMBER,
)
from common.repository.user import USERS

from app.constants import (
    PIONEER_FLOW_TYPE, REPEATER_FLOW_TYPE,
    AVAILABLE_PRODUCTS_JSON_FIELD_NAME, FLOW_TYPE_JSON_FIELD_NAME,
    API_PRODUCT_PATH
)


def test_select_flow_pioneer(
        client,
        pioneer_phone,
        phone_payload
):
    """Тест выбора флоу первичника."""
    response = client.post(API_PRODUCT_PATH, json=phone_payload(pioneer_phone))
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
    response = client.post(API_PRODUCT_PATH, json=phone_payload(repeater_phone))
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    print(USERS[0].phone, repeater_phone)
    assert data[FLOW_TYPE_JSON_FIELD_NAME] == REPEATER_FLOW_TYPE
    assert len(data[AVAILABLE_PRODUCTS_JSON_FIELD_NAME]) > 0


@pytest.mark.parametrize('phone, expected_status', [
    (NULL_PHONE_NUMBER, HTTPStatus.UNPROCESSABLE_ENTITY),
    (EMPTY_PHONE_NUMBER, HTTPStatus.BAD_REQUEST),
    (NOT_STR_PHONE_NUMBER, HTTPStatus.UNPROCESSABLE_ENTITY),
    (INCORRECT_LENGTH_PHONE, HTTPStatus.BAD_REQUEST),
    (INCORRECT_FIRST_SYMBOL_PHONE, HTTPStatus.BAD_REQUEST),
    (INCORRECT_SYMBOL_PHONE, HTTPStatus.BAD_REQUEST),
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
