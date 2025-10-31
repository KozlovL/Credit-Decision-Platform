from tokenize import String

from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.db import Base


class User(Base):
    """Модель пользователя."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_income: Mapped[int] = mapped_column(Integer, nullable=False)
    employment_type: Mapped[str] = mapped_column(String, nullable=False)
    has_property: Mapped[bool] = mapped_column(Boolean, default=False)

    # Один пользователь может иметь много кредитных записей
    credit_notes: Mapped[list['CreditNote']] = relationship(
        'CreditNote',
        back_populates='user',
        cascade='all, delete-orphan'
    )
