import pytest
from common.constants import (
    NULL_PHONE_NUMBER, NOT_STR_PHONE_NUMBER,
    INCORRECT_LENGTH_PHONE, INCORRECT_FIRST_SYMBOL_PHONE,
    INCORRECT_SYMBOL_PHONE, EMPTY_PHONE_NUMBER,
)
from common.schemas.user import UserPhoneWrite
from fastapi import HTTPException
from pydantic import ValidationError


def test_valid_phone(pioneer_phone):
    """Тест валидных номеров телефона."""
    user = UserPhoneWrite(phone=pioneer_phone)
    assert user.phone == pioneer_phone


@pytest.mark.parametrize('phone', (
    pytest.param(
            NULL_PHONE_NUMBER,
            id='null_phone_number',
        ),
    pytest.param(
        NOT_STR_PHONE_NUMBER,
        id='not_str_phone_number',
    ),
))
def test_invalid_type_phone(phone):
    """Тест неверных типов данных номера телефона."""
    with pytest.raises(ValidationError):
        UserPhoneWrite(phone=phone)


@pytest.mark.parametrize('phone', (
    pytest.param(
        INCORRECT_LENGTH_PHONE,
        id='incorrect_length_phone',
    ),
    pytest.param(
            INCORRECT_FIRST_SYMBOL_PHONE,
            id='incorrect_first_symbol_phone',
        ),
    pytest.param(
        INCORRECT_SYMBOL_PHONE,
        id='incorrect_symbol_phone',
    ),
    pytest.param(
        EMPTY_PHONE_NUMBER,
        id='empty_phone_number',
    ),
))
def test_invalid_phone(phone):
    """Тест невалидных номеров телефона."""
    with pytest.raises(ValidationError):
        UserPhoneWrite(phone=phone)
