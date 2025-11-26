import os
from enum import Enum

PIONEER_FLOW_TYPE = 'pioneer'
REPEATER_FLOW_TYPE = 'repeater'
# Берём имя конфига из переменной окружения (по умолчанию — config.local.yaml)
CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.local.yaml')

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    f'../{CONFIG_FILE}'
)
DATA_SERVICE_BASE_URL = 'http://user-data-service:8001'
ANTIFRAUD_PREFIX = '/antifraud'
ANTIFRAUD_TAG = 'antifraud'
MAX_APPLICATIONS_PER_DAY = 3
SIGNIFICANT_INCOME_INCREASE = 2.0
SIGNIFICANT_INCOME_DECREASE = 0.5


class DecisionType(str, Enum):
    PASSED = 'passed'
    REJECTED = 'rejected'


class RejectionReasonType(str, Enum):
    # Общие правила
    MIN_AGE = (
        'User is under minimum age '
        '(User age: {user_age}, min: {min_age}).'
    )
    MIN_INCOME = (
        'Monthly income is below minimum threshold '
        '(User income: {user_income}, min: {min_income}).'
    )
    EMPLOYMENT_STATUS = (
        'Employment type is not allowed '
        '(Current: {employment_type}).'
    )

    # PIONEER
    DAILY_APPLICATION_LIMIT = (
        'Daily application limit exceeded '
        '({count} applications in 24 hours). Max: {max_allowed}.'
    )
    PROPERTY_WITH_LOW_INCOME = (
        'User has property but income is below threshold '
        '(User income: {user_income}, threshold: {income_threshold}).'
    )

    # REPEATER
    OVERDUE_LOANS = 'Account has overdue payments on previous loans.'
    SIGNIFICANT_INCOME_CHANGE = (
        'Significant income change detected '
        '(previous: {prev_income}, current: {current_income}, '
        'change: {change_percent}%).'
    )
    EMPLOYMENT_CHANGE_NOT_ALLOWED = (
        'Employment type changed from full_time to {current_employment_type}.'
    )
