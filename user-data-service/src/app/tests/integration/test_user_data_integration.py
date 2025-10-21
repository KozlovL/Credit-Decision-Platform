from http import HTTPStatus

from app.constants import USER_DATA_URL


def test_get_user_data_success(client, existing_user) -> None:
    """Успешное получение данных пользователя."""
    response = client.get(f'{USER_DATA_URL}?phone={existing_user.phone}')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['phone'] == existing_user.phone
    assert 'profile' in data
    assert 'history' in data
    assert len(data['history']) == 1


def test_get_user_data_not_found(client):
    """Пользователь не найден."""
    response = client.get(f'{USER_DATA_URL}?phone=79999999999')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_put_create_new_user(client, new_user_payload) -> None:
    """Создание нового пользователя."""
    response = client.put(USER_DATA_URL, json=new_user_payload)
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['phone'] == new_user_payload['phone']
    assert data['history'] == []


def test_put_update_existing_profile(client, update_profile_payload) -> None:
    """Обновление профиля существующего пользователя."""
    response = client.put(USER_DATA_URL, json=update_profile_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['profile']['age'] == 35
    assert data['profile']['monthly_income'] == 55000


def test_put_add_new_loan_entry(client, new_loan_entry_payload) -> None:
    """Добавление новой записи в кредитную историю."""
    response = client.put(USER_DATA_URL, json=new_loan_entry_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert any(
        credit_note['loan_id'] == 'loan_2025-10-21_1'
        for credit_note in data['history']
    )


def test_put_update_existing_loan_status(
        client,
        update_loan_status_payload
) -> None:
    """Обновление статуса существующей записи."""
    response = client.put(USER_DATA_URL, json=update_loan_status_payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    updated_loan = next(
        credit_note
        for credit_note in data['history']
        if credit_note['loan_id']
        == update_loan_status_payload['loan_entry']['loan_id']
    )
    assert updated_loan['status'] == 'closed'
    assert (
            updated_loan['close_date']
            == update_loan_status_payload['loan_entry']['close_date']
    )


def test_put_combined_update(client, combined_update_payload) -> None:
    """Комбинированное обновление профиля и добавление новой записи."""
    response = client.put(USER_DATA_URL, json=combined_update_payload)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
    data = response.json()
    assert data['profile']['age'] == 40
    assert any(
        credit_note['loan_id'] == 'loan_2025-10-21_2'
        for credit_note in data['history']
    )


def test_put_invalid_product(client, invalid_product_payload) -> None:
    """Несуществующее название продукта."""
    response = client.put(USER_DATA_URL, json=invalid_product_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_put_invalid_date(client, invalid_date_payload) -> None:
    """Невалидная дата."""
    response = client.put(USER_DATA_URL, json=invalid_date_payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_put_duplicate_loan_id(client, duplicate_loan_id_payload) -> None:
    """Попытка создать запись с уже существующим loan_id."""
    response = client.put(USER_DATA_URL, json=duplicate_loan_id_payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
