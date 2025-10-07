from common.repository.user import add_user
from fastapi import APIRouter

from app.api.scoring_process import (
    check_products_with_score,
    check_user_for_immediate_rejection,
    scoring_process,
)
from app.api.validators import check_if_pioneer, check_products_are_exists
from app.constants import (
    ACCEPTED_STR,
    PIONEER_PREFIX,
    REJECTED_STR,
    SCORING_PREFIX,
    SCORING_TAG,
)
from app.schemas.scoring import (
    ScoringRead,
    ScoringWrite,
)

router = APIRouter(prefix=SCORING_PREFIX, tags=[SCORING_TAG])


@router.post(
    PIONEER_PREFIX,
    response_model=ScoringRead,
    summary='Процесс скоринга для нового пользователя',
)
def scoring_pioneer(
        data: ScoringWrite,
) -> ScoringRead:
    # Проверяем наличие пользователя в "БД"
    check_if_pioneer(phone=data.user_data.phone)
    # Проверяем существуют ли переданные продукты
    check_products_are_exists(products=data.products)
    # Проверяем немедленный отказ
    if check_user_for_immediate_rejection(user_data=data.user_data):
        return ScoringRead(decision=REJECTED_STR, product=None)
    # Считаем оценку пользователя
    user_score = scoring_process(user_data=data.user_data)
    # Проверяем продукты на соответствие оценке пользователя
    available_product = check_products_with_score(
        products=data.products,
        user_score=user_score
    )
    # Если есть подходящий продукт, то выводим его и добавляем пользователя в
    # "БД"
    if available_product is not None:
        # Добавляем пользователя в "БД"
        add_user(phone=data.user_data.phone)
        decision = ACCEPTED_STR
    # Иначе делаем отказ
    else:
        decision = REJECTED_STR
    return ScoringRead(decision=decision, product=available_product)
