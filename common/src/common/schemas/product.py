from pydantic import BaseModel, Field, PositiveInt, ConfigDict

from common.constants import (
    PRODUCT_NAME_MIN_LENGTH, PRODUCT_NAME_MAX_LENGTH,
    INTEREST_RATE_DAILY_MIN_LENGTH, INTEREST_RATE_DAILY_MAX_LENGTH,
)


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

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')
