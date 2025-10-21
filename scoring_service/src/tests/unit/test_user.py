import pytest
from common.constants import PHONE_JSON_FIELD_NAME
from common.schemas.user import UserDataWrite
from pydantic import ValidationError

from app.constants import (
    AGE_FIELD_NAME, MONTHLY_INCOME_FIELD,
    EMPLOYMENT_TYPE_FIELD, HAS_PROPERTY_FIELD,
)
from tests.fixtures.user import (
    VALID_USERDATA_1, VALID_USERDATA_2,
    VALID_USERDATA_3, INVALID_HAS_PROPERTY_USERDATA, INVALID_AGE_USERDATA,
    INVALID_PHONE_USERDATA, INVALID_MONTHLY_INCOME_USERDATA,
    INVALID_EMPLOYMENT_TYPE_USERDATA,
)


@pytest.mark.parametrize(
    (
            PHONE_JSON_FIELD_NAME,
            AGE_FIELD_NAME,
            MONTHLY_INCOME_FIELD,
            EMPLOYMENT_TYPE_FIELD,
            HAS_PROPERTY_FIELD,
    ),
    (
        VALID_USERDATA_1,
        VALID_USERDATA_2,
        VALID_USERDATA_3
    )
)
def test_valid_userdata(
        phone,
        age,
        monthly_income,
        employment_type,
        has_property
):
    """Тест валидных данных пользователя."""
    user = UserDataWrite(
        phone=phone,
        age=age,
        monthly_income=monthly_income,
        employment_type=employment_type,
        has_property=has_property
    )
    assert user.phone == phone
    assert user.age == age
    assert user.monthly_income == monthly_income
    assert user.employment_type == employment_type
    assert user.has_property == has_property


@pytest.mark.parametrize(
    (
            PHONE_JSON_FIELD_NAME,
            AGE_FIELD_NAME,
            MONTHLY_INCOME_FIELD,
            EMPLOYMENT_TYPE_FIELD,
            HAS_PROPERTY_FIELD,
    ),
    (
        INVALID_HAS_PROPERTY_USERDATA,
        INVALID_AGE_USERDATA,
        INVALID_PHONE_USERDATA,
        INVALID_MONTHLY_INCOME_USERDATA,
        INVALID_EMPLOYMENT_TYPE_USERDATA
    )
)
def test_invalid_userdata(
        phone,
        age,
        monthly_income,
        employment_type,
        has_property
):
    """Тест невалидных данных пользователя."""
    with pytest.raises(ValidationError):
        user = UserDataWrite(
            phone=phone,
            age=age,
            monthly_income=monthly_income,
            employment_type=employment_type,
            has_property=has_property
        )
