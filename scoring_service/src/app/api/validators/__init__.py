from http import HTTPStatus

from common.schemas.product import ProductWrite
from fastapi import HTTPException


def check_products_are_exists(
        products: list[ProductWrite],
        available_products: list[str]
) -> None:
    """Проверка существует ли данный на вход продукт."""
    for product in products:
        if product.name not in available_products:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Продукт не существует.'
            )
