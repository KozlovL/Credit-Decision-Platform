import os

from common.constants import API_PREFIX

PIONEER_FLOW_TYPE = 'pioneer'
REPEATER_FLOW_TYPE = 'repeater'
PRODUCT_PREFIX = '/product'
API_PRODUCT_PATH = f'{API_PREFIX}{PRODUCT_PREFIX}'
FLOW_TYPE_JSON_FIELD_NAME = 'flow_type'
AVAILABLE_PRODUCTS_JSON_FIELD_NAME = 'available_products'
PRODUCTS_TAG = 'product'
# Берём имя конфига из переменной окружения (по умолчанию — config.local.yaml)
CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.local.yaml')

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    f'../{CONFIG_FILE}'
)
DATA_SERVICE_BASE_URL = 'http://user-data-service:8001'
PIONEER_PRODUCTS_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    'fixtures/pioneer_products.json'
)
REPEATER_PRODUCTS_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    'fixtures/repeater_products.json'
)
PRODUCTS_KEY = 'products'
