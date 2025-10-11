from http import HTTPStatus

from common.repository.user import get_user_by_phone, User
from fastapi import HTTPException


def get_user_or_404_by_phone(phone: str) -> User | None:
    """Функция, возвращающая пользователя по номеру телефона или ошибку 404."""
    user = get_user_by_phone(phone=phone)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не существует.'
        )
    return user
