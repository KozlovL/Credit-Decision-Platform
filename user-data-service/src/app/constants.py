import re

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
LOAN_ID_REGEX = re.compile(r'^loan_\d{4}-\d{2}-\d{2}_\d+$')
