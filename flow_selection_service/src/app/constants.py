import os
import re

PRODUCT_NAME_MIN_LENGTH = 3
PRODUCT_NAME_MAX_LENGTH = 128
FIRST_PHONE_NUMBER_SYMBOL = '7'
PHONE_NUMBER_LENGTH = 11
INTEREST_RATE_DAILY_MIN_LENGTH = 1
INTEREST_RATE_DAILY_MAX_LENGTH = 64
PIONEER_FLOW_TYPE = 'pioneer'
REPEATER_FLOW_TYPE = 'repeater'
PRODUCT_LIST_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    'product_list.json'
)
# Строка из 11 цифр начинающая на 7
PHONE_REGEX = re.compile(r'^7\d{10}$')
