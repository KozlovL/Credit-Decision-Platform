# Строка из 11 цифр начинающая на 7
import re
from enum import Enum

PHONE_REGEX = re.compile(r'^7\d{10}$')
API_PREFIX = '/api'
PRODUCT_NAME_MIN_LENGTH = 3
PRODUCT_NAME_MAX_LENGTH = 128
PIONEER_PHONE_NUMBER = '71231231231'
INCORRECT_LENGTH_PHONE = '123'
INCORRECT_FIRST_SYMBOL_PHONE = '81111111111'
INCORRECT_SYMBOL_PHONE = '7111111111a'
PHONE_JSON_FIELD_NAME = 'phone'
NULL_PHONE_NUMBER = None
EMPTY_PHONE_NUMBER = ''
AGE_MIN = 0
AGE_MAX = 120


class EmploymentType(str, Enum):
    """Типы занятости."""
    FULL_TIME = 'full_time'
    FREELANCE = 'freelance'
    UNEMPLOYED = 'unemployed'


class CreditStatus(str, Enum):
    """Статус кредита."""
    OPEN = 'open'
    CLOSED = 'closed'


EXISTING_USER_DATA = {
    'phone': '71111111111',
    'age': 30,
    'monthly_income': 6000000,
    'has_property': False,
    'employment_type': EmploymentType.FULL_TIME
}

EXISTING_USER_PRODUCT_DATA = {
    'name': 'MicroLoan',
    'max_amount': 5000000,
    'term_days': 90,
    'interest_rate_daily': 1.5
}

REPEATER_PHONE_NUMBER = EXISTING_USER_DATA['phone']
NOT_STR_PHONE_NUMBER = int(REPEATER_PHONE_NUMBER)
