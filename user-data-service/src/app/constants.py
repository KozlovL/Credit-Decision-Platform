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
TEST_DATABASE_URL = os.getenv("DATABASE_URL")
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    '../config.yaml'
)
