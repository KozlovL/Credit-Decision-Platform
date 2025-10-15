from common.constants import API_PREFIX
from fastapi import APIRouter

from app.api.endpoints import scoring_router

main_router = APIRouter(prefix=API_PREFIX)
main_router.include_router(scoring_router)
