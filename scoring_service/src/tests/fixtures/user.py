from common.constants import NOT_STR_PHONE_NUMBER, EmploymentType

VALID_USERDATA_1 = (
    '71111111112',
    25,
    4500000,
    EmploymentType.FULL_TIME,
    True
)
VALID_USERDATA_2 = (
    '71111111113',
    40,
    1000000,
    EmploymentType.FREELANCE,
    True
)
VALID_USERDATA_3 = (
    '71111111114',
    70,
    999999999,
    EmploymentType.UNEMPLOYED,
    False
)

INVALID_PHONE_USERDATA = (
    NOT_STR_PHONE_NUMBER,
    25,
    4500000,
    EmploymentType.FULL_TIME,
    True
)
INVALID_AGE_USERDATA = (
    '71111111113',
    '999',
    1000000,
    EmploymentType.FREELANCE,
    True
)
INVALID_MONTHLY_INCOME_USERDATA = (
    '71111111114',
    70,
    -25,
    EmploymentType.UNEMPLOYED,
    False
)
INVALID_EMPLOYMENT_TYPE_USERDATA = (
    '71111111113',
    50,
    1000000,
    'working',
    True
)
INVALID_HAS_PROPERTY_USERDATA = (
    '71111111113',
    50,
    1000000,
    EmploymentType.UNEMPLOYED,
    123
)
