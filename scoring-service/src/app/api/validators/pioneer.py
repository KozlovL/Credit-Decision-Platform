from http import HTTPStatus

from fastapi import HTTPException

from app.clients.data_service_client import DataServiceClient


def check_if_pioneer(phone: str, client: DataServiceClient) -> None:
    """Функция, вызывающая исключение, если пользователь - не первичник."""
    try:
        client.get_user_data(phone=phone)
    except HTTPException:
        return None

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='Пользователь не является первичником.'
    )
