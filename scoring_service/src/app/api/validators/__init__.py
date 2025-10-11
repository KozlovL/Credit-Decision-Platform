from http import HTTPStatus

from fastapi import HTTPException

from app.schemas.scoring import ProductWrite


def check_products_are_exists(
        products: list[ProductWrite],
        available_products: list
) -> None:
    """Проверка существует ли данный на вход продукт."""
    for product in products:
        if product.name not in available_products:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Продукт не существует.'
            )
