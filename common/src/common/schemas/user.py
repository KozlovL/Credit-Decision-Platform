from pydantic import (
    ConfigDict, field_validator, BaseModel, PositiveInt, Field,
    StrictBool, ValidationError,
)

from common.constants import (
    PHONE_REGEX, PHONE_JSON_FIELD_NAME, EmploymentType,
    AGE_MIN, AGE_MAX,
)


class UserPhoneWrite(BaseModel):
    """Схема номера телефона пользователя для записи."""
    phone: str

    @field_validator(PHONE_JSON_FIELD_NAME)
    def validate_phone(cls, phone: str) -> str | None:
        if not PHONE_REGEX.match(phone):
            raise ValueError(
                'Номер телефона должен быть строкой из 11 цифр и '
                'начинаться на 7'
            )
        return phone

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')


class ProfileWrite(BaseModel):
    """Схема профиля пользователя для записи."""
    age: int = Field(ge=AGE_MIN, le=AGE_MAX)
    monthly_income: PositiveInt
    employment_type: EmploymentType
    has_property: StrictBool

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')


class ProfileRead(ProfileWrite):
    """Схема профиля пользователя для чтения."""


class UserDataPhoneWrite(UserPhoneWrite, ProfileWrite):
    """Схема данных пользователя с телефоном для записи."""


class UserPhoneRead(UserDataPhoneWrite):
    """Схема номера телефона пользователя для чтения."""
