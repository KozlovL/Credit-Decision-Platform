from json import load

from app.constants import (
    PIONEER_FLOW_TYPE, REPEATER_FLOW_TYPE,
    PRODUCT_LIST_JSON_PATH,
)

# База данных номеров
CUSTOMERS_PHONES = (
    '71111111111',
    '72222222222',
    '73333333333',
    '74444444444',
    '75555555555',
    '76666666666',
    '77777777777',
    '78888888888',
    '79999999999',
)

# база данных типов флоу
FLOW_TYPES = (PIONEER_FLOW_TYPE, REPEATER_FLOW_TYPE)

# База данных доступных продуктов
# Список доступных продуктов получаем из json файла
with open(PRODUCT_LIST_JSON_PATH, 'r', encoding='utf-8') as file:
    AVAILABLE_PRODUCT_LIST = load(file)
