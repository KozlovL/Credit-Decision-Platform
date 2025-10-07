from fastapi import APIRouter

from app.api.scoring_process import (
    check_user_for_immediate_rejection,
    scoring_process, check_products_with_score,
)
from app.schemas.scoring import (
    ScoringRead,
    UserDataWrite, ProductWrite,
)

router = APIRouter(prefix='/scoring', tags=['scoring'])


@router.post(
    '/pioneer',
    response_model=ScoringRead,
    summary='Процесс скоринга для нового пользователя',
)
def scoring_pioneer(
        user_data: UserDataWrite,
        products: list[ProductWrite],
) -> ScoringRead:
    check_if_pioneer(user_data)
    if check_user_for_immediate_rejection(user_data):
        return ScoringRead(decision='rejected', product=None)
    user_score = scoring_process(user_data=user_data)
    available_product = check_products_with_score(
        products=products,
        user_score=user_score
    )
    decision = 'accepted' if available_product is not None else 'rejected'
    return ScoringRead(decision=decision, product=available_product)
