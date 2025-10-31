from datetime import date

from common.constants import CreditStatus, EmploymentType
from sqlalchemy import Integer, Boolean, ForeignKey, Date, String, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.db import Base


class User(Base):
    """Модель пользователя."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_income: Mapped[int] = mapped_column(Integer, nullable=False)
    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType),
        nullable=False
    )
    has_property: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Один пользователь может иметь много кредитных записей
    credit_notes: Mapped[list['CreditNote']] = relationship(
        'CreditNote',
        back_populates='user',
        cascade='all, delete-orphan'
    )


class CreditNote(Base):
    """Модель записи в кредитной истории."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    loan_id: Mapped[str] = mapped_column(String, nullable=False)
    product_name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    term_days: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[CreditStatus] = mapped_column(
        Enum(CreditStatus),
        nullable=False
    )

    close_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Связь с пользователем
    user: Mapped['User'] = relationship('User', back_populates='credit_notes')
