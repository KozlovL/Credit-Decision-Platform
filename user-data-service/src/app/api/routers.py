from common.constants import API_PREFIX
from fastapi import APIRouter

main_router = APIRouter(prefix=API_PREFIX)
main_router.include_router(data_router)
