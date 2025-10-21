from http import HTTPStatus

from common.repository.user import get_users
from fastapi import HTTPException


def check_if_pioneer(phone: str) -> None:
    """Функция, вызывающая исключение, если пользователь - не первичник."""
    for user in get_users():
        if user.phone == phone:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Пользователь уже есть в базе данных.'
            )
