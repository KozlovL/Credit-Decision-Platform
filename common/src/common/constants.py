# Строка из 11 цифр начинающая на 7
import re

PHONE_REGEX = re.compile(r'^7\d{10}$')
API_PREFIX = '/api'
