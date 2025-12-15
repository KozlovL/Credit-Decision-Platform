import os

from common.constants import API_PREFIX

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
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    '../config.yaml'
)
