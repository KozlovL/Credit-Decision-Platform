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
        phone_payload,
        pioneer_products
):
    """Тест выбора флоу первичника."""
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        # Мокаем user-data — возвращает 404 (новый пользователь)
        mock.get(f'/api/user-data?phone={pioneer_phone}').respond(
            status_code=HTTPStatus.NOT_FOUND
        )

        # Мокаем products — возвращает список продуктов для pioneer
        mock.get(f'/api/products?flow_type={PIONEER_FLOW_TYPE}').respond(
            status_code=HTTPStatus.OK,
            json=pioneer_products
        )

        # Делаем запрос
        response = client.post(
            API_PRODUCT_PATH,
            json=phone_payload(pioneer_phone)
        )

    # Проверяем результат
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data[FLOW_TYPE_JSON_FIELD_NAME] == PIONEER_FLOW_TYPE
    assert data[AVAILABLE_PRODUCTS_JSON_FIELD_NAME] == pioneer_products


def test_select_flow_repeater(
        client,
        repeater_phone,
        phone_payload,
        repeater_products
):
    """Тест выбора флоу повторника."""
    with respx.mock(base_url=DATA_SERVICE_BASE_URL) as mock:
        # Мокаем user-data — возвращает 200 (повторник)
        mock.get(f'/api/user-data?phone={repeater_phone}').respond(
            status_code=HTTPStatus.OK,
            json={'phone': repeater_phone, 'profile': {}, 'history': []}
        )

        # Мокаем products — возвращает список продуктов для repeater
        mock.get(f'/api/products?flow_type={REPEATER_FLOW_TYPE}').respond(
            status_code=HTTPStatus.OK,
            json=repeater_products
        )

        # Делаем запрос
        response = client.post(
            API_PRODUCT_PATH,
            json=phone_payload(repeater_phone)
        )

    # Проверяем результат
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data[FLOW_TYPE_JSON_FIELD_NAME] == REPEATER_FLOW_TYPE
    assert data[AVAILABLE_PRODUCTS_JSON_FIELD_NAME] == repeater_products


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
