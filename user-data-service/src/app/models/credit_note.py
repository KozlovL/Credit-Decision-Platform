from datetime import date

from common.constants import CreditStatus
from sqlalchemy import Date, String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.db import Base


class CreditNote(Base):
    """Модель записи в кредитной истории."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    loan_id: Mapped[str] = mapped_column(String, default='')
    product_name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, default=date.today)
    term_days: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default=CreditStatus.OPEN.value)
    close_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Связь с пользователем
    user: Mapped['User'] = relationship('User', back_populates='credit_notes')
