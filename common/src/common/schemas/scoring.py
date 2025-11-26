from pydantic import BaseModel, ConfigDict

from common.schemas.product import ProductWrite
from common.schemas.user import UserDataPhoneWrite, UserPhoneWrite


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
