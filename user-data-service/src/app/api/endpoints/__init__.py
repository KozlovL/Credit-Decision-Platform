from app.api.endpoints.products import router as products_router
from app.api.endpoints.user_data import router as user_data_router

__all__ = [
    'products_router',
    'user_data_router'
]
