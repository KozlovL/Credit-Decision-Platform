from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator

from app.constants import (
    INTEREST_RATE_DAILY_MAX_LENGTH,
    INTEREST_RATE_DAILY_MIN_LENGTH,
    PHONE_REGEX,
    PRODUCT_NAME_MAX_LENGTH,
    PRODUCT_NAME_MIN_LENGTH,
)


class UserPhoneWrite(BaseModel):
    """Схема клиента для записи при выборе флоу."""
    phone: str

    @field_validator('phone')
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


class FlowProductListRead(BaseModel):
    """Схема продуктов для чтения при выборе флоу."""
    flow_type: str
    available_products: list[ProductRead]


class ProductListWrite(BaseModel):
    """Схема продуктов для записи."""
    products: list[ProductRead]


class ScoringRead(BaseModel):
    """Схема результатов скоринга для чтения."""
    decision: str
    product: ProductRead | None


class ScoringUserDataWrite(UserWrite):
    """Схема данных пользователя для записи скоринга."""
    age: PositiveInt
    monthly_income: PositiveInt
    employment_type: str
    has_property: bool


class ProductWrite(ProductRead):
    """Схема продукта для записи."""
    pass
