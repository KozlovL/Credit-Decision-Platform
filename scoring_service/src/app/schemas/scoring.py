from common.schemas.product import ProductRead, ProductWrite
from common.schemas.user import (
    UserDataWrite,
)
from pydantic import BaseModel, ConfigDict


class ScoringRead(BaseModel):
    """Схема результатов скоринга для чтения."""
    decision: str
    product: ProductRead | None


class ScoringWrite(BaseModel):
    """Схема для записи скоринга."""
    user_data: UserDataWrite
    products: list[ProductWrite]

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')
