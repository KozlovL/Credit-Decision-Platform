from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, PositiveInt, ConfigDict

from app.constants import (
    PRODUCT_NAME_MIN_LENGTH,
    PRODUCT_NAME_MAX_LENGTH, FIRST_PHONE_NUMBER_SYMBOL, PHONE_NUMBER_LENGTH,
    INTEREST_RATE_DAILY_MIN_LENGTH, INTEREST_RATE_DAILY_MAX_LENGTH,
)

from src.app.constants import PHONE_REGEX


class CustomerWrite(BaseModel):
    """Схема клиента для записи."""
    phone: str

    @field_validator('phone')
    def validate_phone(cls, phone):
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


class ProductRead(BaseModel):
    """Схема продукта для чтения."""
    name: str = Field(
        ...,
        min_length=PRODUCT_NAME_MIN_LENGTH,
        max_length=PRODUCT_NAME_MAX_LENGTH
    )
    max_amount: PositiveInt
    term_days: PositiveInt
    interest_rate_daily: str = Field(
        ...,
        min_length=INTEREST_RATE_DAILY_MIN_LENGTH,
        max_length=INTEREST_RATE_DAILY_MAX_LENGTH,
    )


class ProductListRead(BaseModel):
    """Схема продуктов для чтения."""
    flow_type: str
    available_products: list[ProductRead]
