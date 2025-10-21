from http import HTTPStatus

from fastapi import HTTPException
from pydantic import ConfigDict, field_validator, BaseModel, PositiveInt, Field

from common.constants import (
    PHONE_REGEX, PHONE_JSON_FIELD_NAME, EmploymentType,
    AGE_MIN, AGE_MAX,
)


class UserPhoneWrite(BaseModel):
    """Схема клиента для записи при выборе флоу."""
    phone: str

    @field_validator(PHONE_JSON_FIELD_NAME)
    def validate_phone(cls, phone: str) -> str | None:
        if not PHONE_REGEX.match(phone):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    'Номер телефона должен быть строкой из 11 цифр и '
                    'начинаться на 7'
                    )
            )
        return phone

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')


class UserDataWrite(UserPhoneWrite):
    """Схема данных пользователя для записи скоринга."""
    age: int = Field(ge=AGE_MIN, le=AGE_MAX)
    monthly_income: PositiveInt
    employment_type: EmploymentType
    has_property: bool

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')
