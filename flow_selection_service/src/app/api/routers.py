from fastapi import APIRouter

from app.api.endpoints import product_router


main_router = APIRouter()
main_router.include_router(product_router)
