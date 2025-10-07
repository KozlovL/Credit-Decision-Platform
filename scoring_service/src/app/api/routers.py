from fastapi import APIRouter

from app.api.endpoints import scoring_router

main_router = APIRouter(prefix='/api')
main_router.include_router(scoring_router)
