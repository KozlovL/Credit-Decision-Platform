"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base
from app.models.user_data import CreditNote, User

__all__ = (
    'Base',
    'CreditNote',
    'User',
)
