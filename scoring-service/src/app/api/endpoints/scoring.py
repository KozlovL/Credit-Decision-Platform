from common.constants import EmploymentType
from common.repository.user import add_user
from common.schemas.user import UserDataPhoneWrite
from fastapi import APIRouter

from app.api.validators import check_products_are_exists
from app.api.validators.pioneer import (
    check_if_pioneer,
)
from app.api.validators.repeater import (
    get_user_or_404_by_phone,
)
from app.constants import (
    MIN_PIONEER_SCORE_FOR_PRODUCT,
    MIN_REPEATER_SCORE_FOR_PRODUCT,
    PIONEER_PREFIX,
    REPEATER_PREFIX,
    SCORING_PREFIX,
    SCORING_TAG,
)
from app.logic.scoring_process import ScoringPioneer, ScoringRepeater
from app.repository.product import (
    get_available_pioneer_product_names,
    get_available_pioneer_products_with_score,
    get_available_repeater_product_names,
    get_available_repeater_products_with_score,
)
from app.schemas.scoring import (
    ScoringRead, ScoringWritePioneer, ScoringWriteRepeater,
)

router = APIRouter(prefix=SCORING_PREFIX, tags=[SCORING_TAG])


@router.post(
    PIONEER_PREFIX,
    response_model=ScoringRead,
    summary='Процесс скоринга для первичника',
)
def scoring_pioneer(
        data: ScoringWritePioneer,
) -> ScoringRead:

    # Проверяем является ли пользователь первичником
    check_if_pioneer(phone=data.user_data.phone)

    # Проверяем существуют ли переданные продукты
    check_products_are_exists(
        products=data.products,
        available_products=get_available_pioneer_product_names()
    )

    # Создаем класс скоринга первичника
    pioneer_scoring = ScoringPioneer(
        user_data=data.user_data,
        products=data.products,
        min_score_for_acceptance=MIN_PIONEER_SCORE_FOR_PRODUCT,
        available_products_with_score=(
            get_available_pioneer_products_with_score()
        )
    )

    # Проводим скоринг
    decision, available_product = pioneer_scoring.get_answer_for_score()

    # Если есть подходящий продукт, то решение положительное и добавляем
    # запись в кредитную историю пользователя
    if available_product is not None:
        # Добавляем пользователя в "БД"
        user = add_user(user_data=data.user_data)
        # Добавляем запись в кредитную историю пользователя
        user.add_credit_note(
            product_data=available_product,
        )

    return ScoringRead(decision=decision, product=available_product)


@router.post(
    REPEATER_PREFIX,
    response_model=ScoringRead,
    summary='Процесс скоринга для повторника',
)
def scoring_repeater(
        data: ScoringWriteRepeater,
) -> ScoringRead:

    phone = data.phone
    products = data.products

    # Пытаемся получить пользователя из БД
    user = get_user_or_404_by_phone(phone=phone)

    # Проверяем существуют ли переданные продукты
    check_products_are_exists(
        products=products,
        available_products=get_available_repeater_product_names()
    )

    # Создаем класс скоринга повторника
    repeater_scoring = ScoringRepeater(
        user_data=UserDataPhoneWrite(
            phone=user.phone,
            age=user.age,
            monthly_income=user.monthly_income,
            employment_type=EmploymentType(user.employment_type),
            has_property=user.has_property,
        ),
        products=products,
        min_score_for_acceptance=MIN_REPEATER_SCORE_FOR_PRODUCT,
        available_products_with_score=(
            get_available_repeater_products_with_score()
        ),
        credit_history=user.credit_history,
    )

    # Проводим скоринг
    decision, available_product = repeater_scoring.get_answer_for_score()

    # Если есть подходящий продукт, то решение положительное и добавляем
    # запись в кредитную историю пользователя
    if available_product is not None:
        # Добавляем запись в кредитную историю пользователя
        user.add_credit_note(
            product_data=available_product
        )

    return ScoringRead(decision=decision, product=available_product)
