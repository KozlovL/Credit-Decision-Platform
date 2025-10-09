import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.constants import (
    INCORRECT_LENGTH_PHONE,
    INCORRECT_FIRST_SYMBOL_PHONE, INCORRECT_SYMBOL_PHONE, NULL_PHONE_NUMBER,
    EMPTY_PHONE_NUMBER, NOT_STR_PHONE_NUMBER,
)
from app.schemas.product import CustomerWrite


def test_valid_phone(pioneer_phone):
    customer = CustomerWrite(phone=pioneer_phone)
    assert customer.phone == pioneer_phone


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
    with pytest.raises(ValidationError):
        CustomerWrite(phone=phone)


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
    with pytest.raises(HTTPException):
        CustomerWrite(phone=phone)
