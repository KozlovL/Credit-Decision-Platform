from common.constants import API_PREFIX
from fastapi import APIRouter

from app.api.endpoints import antifraud_router

main_router = APIRouter(prefix=API_PREFIX)
main_router.include_router(antifraud_router)
