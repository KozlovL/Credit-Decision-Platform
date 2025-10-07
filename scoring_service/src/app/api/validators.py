from http import HTTPStatus

from common.repository.product import AVAILABLE_PRODUCT_LIST
from common.repository.user import USERS_PHONES
from fastapi import HTTPException

from app.schemas.scoring import ProductWrite


def check_if_pioneer(phone: str) -> None:
    """Функция, проверяющая наличие пользователя в БД."""
    if phone in USERS_PHONES:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь уже есть в базе данных.'
        )


def check_products_are_exists(products: list[ProductWrite]) -> None:
    """Проверка существует ли данный на вход продукт."""
    for product in products:
        if product.model_dump() not in AVAILABLE_PRODUCT_LIST:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Продукт не существует.'
            )
