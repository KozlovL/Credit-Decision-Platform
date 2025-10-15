# База данных доступных продуктов
# Список доступных продуктов получаем из json файла
from json import load

from common.constants import PRODUCT_LIST_JSON_PATH

with open(PRODUCT_LIST_JSON_PATH, encoding='utf-8') as file:
    AVAILABLE_PRODUCT_LIST = load(file)
