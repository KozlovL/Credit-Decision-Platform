# Список доступных продуктов получаем из json файла
from json import load

from common.schemas.product import ProductRead

from app.constants import (
    PIONEER_PRODUCTS_JSON_PATH,
    REPEATER_PRODUCTS_JSON_PATH,
)

with open(PIONEER_PRODUCTS_JSON_PATH, encoding='utf-8') as file:
    PIONEER_PRODUCTS = load(file)

with open(REPEATER_PRODUCTS_JSON_PATH, encoding='utf-8') as file:
    REPEATER_PRODUCTS = load(file)


def get_available_pioneer_products() -> list[ProductRead]:
    """Получение всех доступных первичнику продуктов."""
    return [ProductRead(**product) for product in PIONEER_PRODUCTS]


def get_available_repeater_products() -> list[ProductRead]:
    """Получение всех доступных повторнику продуктов."""
    return [ProductRead(**product) for product in REPEATER_PRODUCTS]
