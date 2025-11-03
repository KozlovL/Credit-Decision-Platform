from http import HTTPStatus

import pytest
from common.constants import LOAN_ID_REGEX

from app.constants import USER_DATA_URL



@pytest.mark.asyncio
async def test_get_user_data_success(client, existing_user):
    """Успешное получение данных пользователя."""
    response = await client.get(f'{USER_DATA_URL}?phone={existing_user.phone}')
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['phone'] == existing_user.phone
    assert 'profile' in data
    assert 'history' in data
    assert len(data['history']) == 1
    assert LOAN_ID_REGEX.match(data['history'][0]['loan_id'])

@pytest.mark.asyncio
async def test_get_user_data_not_found(client):
    """Пользователь не найден."""
    response = await client.get(f'{USER_DATA_URL}?phone=79999999999')
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_put_create_new_user(client, new_user_payload):
    """Создание нового пользователя."""
    response = await client.put(USER_DATA_URL, json=new_user_payload)
    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data['phone'] == new_user_payload['phone']
    assert data.get('history', []) == []


@pytest.mark.asyncio
async def test_put_update_existing_profile(client, update_profile_payload):
    """Обновление профиля существующего пользователя."""
    response = await client.put(USER_DATA_URL, json=update_profile_payload)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['profile']['age'] == 35
    assert data['profile']['monthly_income'] == 55000


@pytest.mark.asyncio
async def test_put_add_new_loan_entry(client, new_loan_entry_payload):
    """Добавление новой записи в кредитную историю."""
    response = await client.put(USER_DATA_URL, json=new_loan_entry_payload)
    
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert any(
        note['loan_id'] == new_loan_entry_payload['loan_entry']['loan_id']
        for note in data['history']
    )


@pytest.mark.asyncio
async def test_put_update_existing_loan_status(client, update_loan_status_payload):
    """Обновление статуса существующей записи."""
    response = await client.put(USER_DATA_URL, json=update_loan_status_payload)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    updated_loan = next(
        note for note in data['history']
        if note['loan_id'] == update_loan_status_payload['loan_entry']['loan_id']
    )
    assert updated_loan['status'] == 'closed'
    assert updated_loan['close_date'] == update_loan_status_payload['loan_entry']['close_date']


@pytest.mark.asyncio
async def test_put_combined_update(client, combined_update_payload):
    """Комбинированное обновление профиля и добавление новой записи."""
    response = await client.put(USER_DATA_URL, json=combined_update_payload)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)

    data = response.json()
    assert data['profile']['age'] == 40
    assert any(
        LOAN_ID_REGEX.match(note['loan_id'])
        for note in data['history']
    )


@pytest.mark.asyncio
async def test_put_invalid_product(client, invalid_product_payload):
    """Несуществующее название продукта."""
    response = await client.put(USER_DATA_URL, json=invalid_product_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_put_invalid_date(client, invalid_date_payload):
    """Невалидная дата."""
    response = await client.put(USER_DATA_URL, json=invalid_date_payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_put_duplicate_loan_id(client, duplicate_loan_id_payload):
    """Попытка создать запись с уже существующим loan_id."""
    response = await client.put(USER_DATA_URL, json=duplicate_loan_id_payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
