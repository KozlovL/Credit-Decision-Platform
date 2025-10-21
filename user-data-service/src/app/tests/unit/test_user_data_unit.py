import pytest
from pydantic import ValidationError
from common.schemas.user import UserDataPhoneWrite, ProfileWrite
from common.constants import EmploymentType


def test_valid_user_profile():
    """Тест валидного профиля пользователя."""
    profile = ProfileWrite(
        age=30,
        monthly_income=50000,
        employment_type=EmploymentType.FULL_TIME,
        has_property=True
    )
    user = UserDataPhoneWrite(
        phone='79123456789',
        **profile.model_dump()
    )
    assert user.age == 30
    assert user.monthly_income == 50000
    assert user.employment_type == EmploymentType.FULL_TIME


@pytest.mark.parametrize(
    'phone, age, monthly_income, employment_type, has_property',
    [
        ('123', 30, 50000, EmploymentType.FULL_TIME, True),
        ('79123456789', -1, 50000, EmploymentType.FULL_TIME, True),
        ('79123456789', 30, -500, EmploymentType.FULL_TIME, True),
        ('79123456789', 30, 50000, 'unknown', True),
        ('79123456789', 30, 50000, EmploymentType.FULL_TIME, 'yes'),
    ]
)
def test_invalid_user_profile(
        phone,
        age,
        monthly_income,
        employment_type,
        has_property
):
    """Тест неверного профиля пользователя."""
    with pytest.raises(ValidationError):
        UserDataPhoneWrite(
            phone=phone,
            age=age,
            monthly_income=monthly_income,
            employment_type=employment_type,  # type: ignore
            has_property=has_property
        )
