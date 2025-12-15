from pydantic import BaseModel, Field, PositiveInt, ConfigDict, PositiveFloat

from common.constants import (
    PRODUCT_NAME_MIN_LENGTH, PRODUCT_NAME_MAX_LENGTH,
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
    interest_rate_daily: PositiveFloat

    # Чтобы схема могла принимать ORM-объекты
    model_config = ConfigDict(from_attributes=True)


class ProductWrite(ProductRead):
    """Схема продукта для записи."""

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')
