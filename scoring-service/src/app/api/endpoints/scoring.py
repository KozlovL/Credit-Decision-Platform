import logging

from common.constants import EmploymentType
from common.schemas.user import UserDataPhoneWrite, CreditHistoryRead
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.validators import check_products_are_exists
from app.api.validators.pioneer import (
    check_if_pioneer,
)
from app.clients.data_service_client import (
    DataServiceClient,
    get_data_service_client,
)
from app.constants import (
    MIN_PIONEER_SCORE_FOR_PRODUCT,
    MIN_REPEATER_SCORE_FOR_PRODUCT,
    PIONEER_PREFIX,
    REPEATER_PREFIX,
    SCORING_PREFIX,
    SCORING_TAG, PIONEER_SCORING_URL,
)
from app.logic.scoring_process import (
    ScoringPioneer, ScoringRepeater,
)
from app.repository.product import (
    get_available_pioneer_product_names,
    get_available_pioneer_products_with_score,
    get_available_repeater_product_names,
    get_available_repeater_products_with_score,
)
from app.repository.user import put_profile_and_loan, put_loan
from app.schemas.scoring import (
    ScoringRead,
    ScoringWritePioneer,
    ScoringWriteRepeater,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix=SCORING_PREFIX, tags=[SCORING_TAG])


@router.post(
    PIONEER_PREFIX,
    response_model=ScoringRead,
    summary='Процесс скоринга для первичника',
)
def scoring_pioneer(
        data: ScoringWritePioneer,
        client: DataServiceClient = Depends(get_data_service_client),
) -> ScoringRead:

    # Проверяем является ли пользователь первичником
    check_if_pioneer(phone=data.user_data.phone, client=client)

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

        # Достаем отдельно телефон и профиль
        profile = data.user_data.model_dump()
        phone = profile.pop('phone')

        # Создаем пользователя и запись в кредитной истории
        try:
            put_profile_and_loan(
                phone=phone,
                user_data=profile,
                available_product=available_product,
                client=client,
            )
        except HTTPException as error:
            logger.error(
                f'Ошибка сохранения профиля в user-data-service '
                f'(телефон={phone}, '
                f'endpoint={PIONEER_SCORING_URL}, '
                f'код={error.status_code}'
                f'): {error.detail}'
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail='Ошибка при сохранении данных в user-data-service'
            ) from error

    return ScoringRead(decision=decision, product=available_product)


@router.post(
    REPEATER_PREFIX,
    response_model=ScoringRead,
    summary='Процесс скоринга для повторника',
)
def scoring_repeater(
        data: ScoringWriteRepeater,
        client: DataServiceClient = Depends(get_data_service_client),
) -> ScoringRead:

    phone = data.phone
    products = data.products

    # Пытаемся получить пользователя из БД
    try:
        user_data = client.get_user_data(phone=phone)
    except HTTPException as error:
        logger.error(
            f'Ошибка при получении данных из user-data-service '
            f'(телефон={phone}, '
            f'endpoint={PIONEER_SCORING_URL}, '
            f'код={error.status_code}'
            f'): {error.detail}'
        )
        raise HTTPException(
            status_code=error.status_code,
            detail='Ошибка при получении данных из user-data-service'
        ) from error

    # Проверяем существуют ли переданные продукты
    check_products_are_exists(
        products=products,
        available_products=get_available_repeater_product_names()
    )

    profile = user_data['profile']
    credit_history = user_data['history']

    # Создаем класс скоринга повторника
    repeater_scoring = ScoringRepeater(
        user_data=UserDataPhoneWrite(
            phone=user_data['phone'],
            age=profile['age'],
            monthly_income=profile['monthly_income'],
            employment_type=EmploymentType(profile['employment_type']),
            has_property=profile['has_property'],
        ),
        products=products,
        min_score_for_acceptance=MIN_REPEATER_SCORE_FOR_PRODUCT,
        available_products_with_score=(
            get_available_repeater_products_with_score()
        ),
        credit_history=[CreditHistoryRead(
            **credit_note
        ) for credit_note in credit_history],
    )

    # Проводим скоринг
    decision, available_product = repeater_scoring.get_answer_for_score()

    # Если есть подходящий продукт, то решение положительное и добавляем
    # запись в кредитную историю пользователя
    if available_product is not None:
        # Добавляем запись в кредитную историю пользователя
        try:
            put_loan(
                phone=phone,
                available_product=available_product,
                client=client,
            )
        except HTTPException as error:
            logger.error(
                f'Ошибка сохранения записи в user-data-service '
                f'(телефон={phone}, '
                f'endpoint={PIONEER_SCORING_URL}, '
                f'код={error.status_code}'
                f'): {error.detail}'
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail='Ошибка при сохранении данных в user-data-service'
            ) from error

    return ScoringRead(decision=decision, product=available_product)
