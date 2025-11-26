from datetime import date
from typing import Any, Self

from pydantic import (
    ConfigDict, field_validator, BaseModel, PositiveInt, Field,
    StrictBool, model_validator,
)

from common.constants import (
    PHONE_REGEX, PHONE_JSON_FIELD_NAME, EmploymentType,
    AGE_MIN, AGE_MAX, CreditStatus, LOAN_ID_REGEX,
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


class ValidateStatusAndCloseDateMixin:
    """Миксин с валидацией статуса и даты закрытия кредита."""
    close_date: Any
    status: Any

    @model_validator(mode='after')
    def validate_status_close_date(self) -> Self:
        """Валидация поля close_date относительно статуса."""
        if (
            (
                self.close_date is None
                and self.status == CreditStatus.CLOSED
            )
            or
                (
                    self.close_date is not None
                    and self.status != CreditStatus.CLOSED
                )
        ):
            raise ValueError(
                'Поле close_date может быть пустым только при открытом '
                'статусе кредита и наоборот.'
            )
        return self


class CreditHistoryRead(
    BaseModel,
    ValidateStatusAndCloseDateMixin,
):
    """Схема кредитной истории для чтения."""

    loan_id: str
    product_name: str
    amount: PositiveInt
    issue_date: date
    term_days: PositiveInt
    status: CreditStatus
    close_date: date | None

    @field_validator('loan_id')
    def validate_phone(cls, value: str) -> str | None:
        if not LOAN_ID_REGEX.match(value):
            raise ValueError(
                'Неверный формат loan_id. '
                'Верный формат выглядит так - loan_{phone}_{timestamp}'
            )
        return value
