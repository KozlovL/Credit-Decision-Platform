from common.schemas.product import ProductRead
from pydantic import BaseModel


class ProductListRead(BaseModel):
    """Схема продуктов для чтения."""
    flow_type: str
    available_products: list[ProductRead]
