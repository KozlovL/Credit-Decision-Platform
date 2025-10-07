from enum import Enum

from common.constants import API_PREFIX

ACCEPTED_STR = 'accepted'
REJECTED_STR = 'rejected'
PIONEER_PREFIX = '/pioneer'
SCORING_PREFIX = '/scoring'
SCORING_TAG = 'scoring'
ADULT_AGE = 18
MONTHLY_INCOME_FIELD = 'monthly_income'
AGE_MIN = 0
AGE_MAX = 150
LOW_INCOME = 1000000
AVERAGE_INCOME = 3000000
HIGH_INCOME = 5000000
FULL_TIME_STR = 'full_time'
FREELANCE_STR = 'freelance'
UNEMPLOYED_STR = 'unemployed'
AVERAGE_AGE = 25
OLD_AGE = 40
MICROLOAN_STR = 'MicroLoan'
AGE_FIELD_NAME = 'age'
EMPLOYMENT_TYPE_FIELD = 'employment_type'
HAS_PROPERTY_FIELD = 'has_property'
PIONEER_SCORING_URL = f'{API_PREFIX}{SCORING_PREFIX}{PIONEER_PREFIX}'
QUICK_MONEY_STR = 'QuickMoney'
CONSUMER_LOAN_STR = 'ConsumerLoan'


class EmploymentType(str, Enum):
    """Типы занятости для схемы."""
    full_time = FULL_TIME_STR
    freelance = FREELANCE_STR
    unemployed = UNEMPLOYED_STR
