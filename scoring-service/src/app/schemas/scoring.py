from common.schemas.product import (
    ProductRead,
    ProductWrite,
)
from common.schemas.user import (
    UserDataPhoneWrite,
    UserPhoneWrite,
)
from pydantic import BaseModel, ConfigDict


class ScoringRead(BaseModel):
    """Схема результатов скоринга для чтения."""
    decision: str
    product: ProductRead | None


class ProductListMixin:
    """Миксин, содержащий список продуктов."""

    products: list[ProductWrite]


class ScoringWritePioneer(ProductListMixin, BaseModel):
    """Схема для записи скоринга первичника."""
    user_data: UserDataPhoneWrite

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')


class ScoringWriteRepeater(ProductListMixin, UserPhoneWrite):
    """Схема для записи скоринга повторника."""

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')
