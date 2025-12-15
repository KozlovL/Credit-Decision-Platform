from common.schemas.product import (
    ProductRead,
)
from pydantic import BaseModel


class ScoringRead(BaseModel):
    """Схема результатов скоринга для чтения."""
    decision: str
    product: ProductRead | None
