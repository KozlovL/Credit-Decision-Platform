import os
from enum import IntEnum

from common.constants import API_PREFIX

ACCEPTED_STR = 'accepted'
REJECTED_STR = 'rejected'
PIONEER_PREFIX = '/pioneer'
REPEATER_PREFIX = '/repeater'
SCORING_PREFIX = '/scoring'
SCORING_TAG = 'scoring'
MONTHLY_INCOME_FIELD = 'monthly_income'
AGE_FIELD_NAME = 'age'
EMPLOYMENT_TYPE_FIELD = 'employment_type'
HAS_PROPERTY_FIELD = 'has_property'
PIONEER_SCORING_URL = f'{API_PREFIX}{SCORING_PREFIX}{PIONEER_PREFIX}'
REPEATER_SCORING_URL = f'{API_PREFIX}{SCORING_PREFIX}{REPEATER_PREFIX}'
MIN_PIONEER_SCORE_FOR_PRODUCT = 5
MIN_REPEATER_SCORE_FOR_PRODUCT = 6
DATE_FORMAT = '%Y-%m-%d'
CREDIT_EXPIRATION_DAYS = 180
FIRST_CREDIT_DAYS_TO_GET_SCORE = 365
MICROLOAN_STR = 'MicroLoan'
QUICK_MONEY_STR = 'QuickMoney'
CONSUMER_LOAN_STR = 'ConsumerLoan'
LOYALTY_LOAN_STR = 'LoyaltyLoan'
ADVANTAGE_PLUS_STR = 'AdvantagePlus'
PRIME_CREDIT_STR = 'PrimeCredit'
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    'config/config.yaml'
)
DATA_SERVICE_BASE_URL = 'http://localhost:8001'


class AgeType(IntEnum):
    """Типы возраста."""
    ADULT_AGE = 18
    AVERAGE_AGE = 26
    OLD_AGE = 41


class MonthlyIncomeType(IntEnum):
    """Типы заработка."""
    LOW_INCOME = 1000000
    AVERAGE_INCOME = 3000000
    HIGH_INCOME = 5000000


class LastCreditAmountTypes(IntEnum):
    """Типы объема последнего кредита."""
    LOW_AMOUNT = 5000000
    AVERAGE_AMOUNT = 10000001
