"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base
from app.models import CreditNote, Products, User

__all__ = (
    'Base',
    'CreditNote',
    'Products',
    'User'
)
