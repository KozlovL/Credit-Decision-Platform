import os

from common.constants import API_PREFIX
from dotenv import load_dotenv

load_dotenv()

USER_DATA_PREFIX = '/user-data'
USER_DATA_TAG = 'user-data'
USER_DATA_URL = f'{API_PREFIX}{USER_DATA_PREFIX}'
AVAILABLE_PRODUCTS = (
    'MicroLoan',
    'QuickMoney',
    'ConsumerLoan',
    'LoyaltyLoan',
    'AdvantagePlus',
    'PrimeCredit'
)
TEST_DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{os.getenv("POSTGRES_TEST_USER")}:{os.getenv("POSTGRES_TEST_PASSWORD")}'
    f'@{os.getenv("POSTGRES_TEST_HOST")}:{os.getenv("POSTGRES_TEST_PORT")}/'
    f'{os.getenv("POSTGRES_TEST_DB")}'
)

# Берём имя конфига из переменной окружения (по умолчанию — config.local.yaml)
CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.local.yaml')

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    f'../{CONFIG_FILE}'
)

PRODUCTS_PREFIX = '/products'
PRODUCTS_TAG = 'products'
PIONEER_PRODUCTS_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    'fixtures/pioneer_products.json'
)
REPEATER_PRODUCTS_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    'fixtures/repeater_products.json'
)
