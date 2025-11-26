# Строка из 11 цифр начинающая на 7
import re
from enum import Enum, IntEnum

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
LOAN_ID_REGEX = re.compile(r'^loan_7\d{10}_\d{14}$')
CREDIT_EXPIRATION_DAYS = 180


class EmploymentType(str, Enum):
    """Типы занятости."""
    FULL_TIME = 'full_time'
    FREELANCE = 'freelance'
    UNEMPLOYED = 'unemployed'


class CreditStatus(str, Enum):
    """Статус кредита."""
    OPEN = 'open'
    CLOSED = 'closed'
    OVERDUE = 'overdue'


class ClientType(str, Enum):
    """Типы клиентов."""
    PIONEER = 'pioneer'
    REPEATER = 'repeater'



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
