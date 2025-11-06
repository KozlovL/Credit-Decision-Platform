from common.constants import ClientType
from sqlalchemy import CheckConstraint, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Products(Base):  # type: ignore[misc]
    """Модель продукта."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    max_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    term_days: Mapped[int] = mapped_column(Integer, nullable=False)
    interest_rate_daily: Mapped[float] = mapped_column(Float, nullable=False)
    flow_type: Mapped[ClientType] = mapped_column(
        Enum(ClientType),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint('max_amount > 0', name='check_max_amount_positive'),
        CheckConstraint('term_days > 0', name='check_term_days_positive'),
        CheckConstraint('interest_rate_daily > 0', name='check_interest_rate_positive'),
    )
