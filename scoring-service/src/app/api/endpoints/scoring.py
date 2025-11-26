import logging
from datetime import UTC, datetime

from common.constants import CreditStatus, EmploymentType
from common.schemas.scoring import ScoringWritePioneer, ScoringWriteRepeater
from common.schemas.user import CreditHistoryRead, UserDataPhoneWrite
from fastapi import APIRouter, Depends, Request

from app.api.validators import check_products_are_exists
from app.api.validators.pioneer import check_if_pioneer
from app.clients.data_service_client import (DataServiceClient,
                                             get_data_service_client)
from app.constants import (MIN_PIONEER_SCORE_FOR_PRODUCT,
                           MIN_REPEATER_SCORE_FOR_PRODUCT, PIONEER_PREFIX,
                           REPEATER_PREFIX, SCORING_PREFIX, SCORING_TAG)
from app.logic.scoring_process import (ScoringPioneer, ScoringRepeater,
                                       generate_loan_id)
from app.repository.product import (get_available_pioneer_product_names,
                                    get_available_pioneer_products_with_score,
                                    get_available_repeater_product_names,
                                    get_available_repeater_products_with_score)
from app.schemas.scoring import ScoringRead

router = APIRouter(prefix=SCORING_PREFIX, tags=[SCORING_TAG])


@router.post(PIONEER_PREFIX, response_model=ScoringRead)
async def scoring_pioneer(
        data: ScoringWritePioneer,
        request: Request,
        client: DataServiceClient = Depends(get_data_service_client),
) -> ScoringRead:
    # Получаем продюсера из app.state
    producer = request.app.state.producer

    # Проверяем на первичника
    check_if_pioneer(phone=data.user_data.phone, client=client)
    check_products_are_exists(
        products=data.products,
        available_products=get_available_pioneer_product_names()
    )

    # Создаем класс скоринга
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

    if available_product is not None:
        # Достаем отдельно телефон и профиль
        profile = data.user_data.model_dump()
        phone = profile.pop('phone')

        # Сообщение в Kafka
        message = {
            'version': 1,  # версия схемы
            'event_type': 'pioneer_accepted',  # тип события
            'phone': phone,
            'profile': profile,  # словарь для ProfileWrite
            'loan_entry': {  # словарь для LoanCreate
                'loan_id': generate_loan_id(phone=phone),
                'product_name': available_product.name,
                'amount': available_product.max_amount,
                'issue_date': str(datetime.now(UTC).date()),
                'term_days': available_product.term_days,
                'status': CreditStatus.OPEN,
                'close_date': None
            },
            'occurred_at': datetime.now(UTC).isoformat()
        }
        try:
            await producer.send(
                message
            )
        except Exception as exc:
            logging.error(
                f'Ошибка отправки pioneer_accepted в Kafka '
                f'(phone={data.user_data.phone}): {exc}"'
            )

    return ScoringRead(decision=decision, product=available_product)


@router.post(REPEATER_PREFIX, response_model=ScoringRead)
async def scoring_repeater(
        data: ScoringWriteRepeater,
        request: Request,
        client: DataServiceClient = Depends(get_data_service_client),
) -> ScoringRead:
    producer = request.app.state.producer

    phone = data.phone
    products = data.products

    try:
        user_data = client.get_user_data(phone=phone)
    except Exception as exc:
        logging.error(
            f'Ошибка при получении данных из user-data-service '
            f'(phone={phone}): {exc}'
        )
        raise exc from exc

    check_products_are_exists(
        products=products,
        available_products=get_available_repeater_product_names()
    )

    profile = user_data['profile']
    credit_history = user_data['history']

    user_data_model = UserDataPhoneWrite(
        phone=user_data['phone'],
        age=profile['age'],
        monthly_income=profile['monthly_income'],
        employment_type=EmploymentType(profile['employment_type']),
        has_property=profile['has_property'],
    )

    repeater_scoring = ScoringRepeater(
        user_data=user_data_model,
        products=products,
        min_score_for_acceptance=MIN_REPEATER_SCORE_FOR_PRODUCT,
        available_products_with_score=(
            get_available_repeater_products_with_score()
        ),
        credit_history=[CreditHistoryRead(**ch) for ch in credit_history]
    )

    decision, available_product = repeater_scoring.get_answer_for_score()

    if available_product is not None:
        message = {
            'version': 1,
            'event_type': 'repeater_accepted',
            'phone': phone,
            'loan_entry': {
                'loan_id': generate_loan_id(phone=phone),
                'product_name': available_product.name,
                'amount': available_product.max_amount,
                'issue_date': str(datetime.now(UTC).date()),
                'term_days': available_product.term_days,
                'status': CreditStatus.OPEN,
                'close_date': None
            },
            'occurred_at': datetime.now(UTC).isoformat()
        }

        try:
            await producer.send(message)
        except Exception as exc:
            logging.error(
                f'Ошибка отправки repeater_accepted в Kafka '
                f'(phone={phone}): {exc}'
            )

    return ScoringRead(decision=decision, product=available_product)
