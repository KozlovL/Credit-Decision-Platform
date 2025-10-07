from common.schemas.product import ProductRead
from common.schemas.user import UserPhoneWrite
from pydantic import BaseModel, ConfigDict, PositiveInt, Field

from app.constants import (
    AGE_MAX,
    AGE_MIN,
    EmploymentType,
)


class ScoringRead(BaseModel):
    """Схема результатов скоринга для чтения."""
    decision: str
    product: ProductRead | None


class ScoringUserDataWrite(UserPhoneWrite):
    """Схема данных пользователя для записи скоринга."""
    age: int = Field(ge=AGE_MIN, le=AGE_MAX)
    monthly_income: PositiveInt
    employment_type: EmploymentType
    has_property: bool

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')


class ProductWrite(ProductRead):
    """Схема продукта для записи."""


class ScoringWrite(BaseModel):
    """Схема для записи скоринга."""
    user_data: ScoringUserDataWrite
    products: list[ProductWrite]

    # Выбрасываем ошибку при передаче лишних полей
    model_config = ConfigDict(extra='forbid')
