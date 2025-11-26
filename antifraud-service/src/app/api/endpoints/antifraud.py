import logging

from common.schemas.user import CreditHistoryRead, ProfileWrite
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.clients.data_service_client import DataServiceClient, get_data_service_client
from app.clients.redis_client import RedisClient, get_redis_client
from app.constants import (
    ANTIFRAUD_PREFIX,
    ANTIFRAUD_TAG,
    PIONEER_FLOW_TYPE,
    REPEATER_FLOW_TYPE,
    DecisionType,
)
from app.logic.antifraud import AntifraudPioneer, AntifraudRepeater
from app.schemas.antifraud import (
    AntifraudRead,
    PioneerAntifraudWrite,
    RepeaterAntifraudWrite,
)

router = APIRouter(prefix=ANTIFRAUD_PREFIX, tags=[ANTIFRAUD_TAG])


@router.post(
    f'/{PIONEER_FLOW_TYPE}/check',
    response_model=AntifraudRead,
    summary='Проверка первичного пользователя на немедленный отказ',
)
async def check_pioneer(
    data: PioneerAntifraudWrite,
    redis: RedisClient = Depends(get_redis_client)
) -> AntifraudRead:
    user_data = data.user_data.model_dump()
    phone = user_data.pop('phone')

    antifraud = AntifraudPioneer(
        current_profile=ProfileWrite(**user_data),
        phone=phone,
        redis_client=redis
    )
    decision, reasons = await antifraud.run_checks()
    return AntifraudRead(decision=DecisionType(decision), reasons=reasons)


@router.post(
    f'/{REPEATER_FLOW_TYPE}/check',
    response_model=AntifraudRead,
    summary='Проверка повторного пользователя на немедленный отказ',
)
async def check_repeater(
    data: RepeaterAntifraudWrite,
    data_service_client: DataServiceClient = Depends(get_data_service_client),
) -> AntifraudRead:
    phone = data.phone

    # Получаем пользователя из сервиса данных
    try:
        user_data = await data_service_client.get_user_data(phone=phone)
    except Exception as exc:
        logging.error(
            f'Ошибка при получении данных из user-data-service '
            f'(phone={phone}): {exc}'
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f'Ошибка при обращении к сервису данных для phone={phone}'
        ) from exc

    # Извлекаем кредитную историю, прошлый и текущий профиль
    credit_history = user_data['history']
    previous_profile = user_data['profile']
    current_profile = data.current_profile

    # Инициализируем антифрод повторника
    antifraud = AntifraudRepeater(
        phone=user_data['phone'],
        credit_history=[
            CreditHistoryRead(**ch)
            for ch in credit_history
        ],
        previous_profile=ProfileWrite(**previous_profile),
        current_profile=current_profile
    )

    decision, reasons = await antifraud.run_checks()
    return AntifraudRead(decision=DecisionType(decision), reasons=reasons)
