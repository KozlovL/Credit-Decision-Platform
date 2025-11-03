import logging

from common.schemas.user import UserPhoneWrite
from fastapi import APIRouter, Depends, HTTPException

from app.clients.data_service_client import (
    DataServiceClient,
    get_data_service_client,
)
from app.constants import (
    PIONEER_FLOW_TYPE,
    PRODUCT_PREFIX,
    PRODUCTS_TAG,
    REPEATER_FLOW_TYPE,
)
from app.logic.user import is_repeater
from app.repository.products import (
    get_available_pioneer_products,
    get_available_repeater_products,
)
from app.schemas.product import FlowProductRead

router = APIRouter(prefix=PRODUCT_PREFIX, tags=[PRODUCTS_TAG])


logger = logging.getLogger(__name__)


@router.post(
    '',
    response_model=FlowProductRead,
    summary='Выбор флоу по номеру телефона',
)
def select_flow(
        user: UserPhoneWrite,
        client: DataServiceClient = Depends(get_data_service_client),
) -> FlowProductRead:

    try:
        # Если пользователь повторник...
        if is_repeater(phone=user.phone, client=client):
            flow_type = REPEATER_FLOW_TYPE
            available_products = get_available_repeater_products()
        else:
            flow_type = PIONEER_FLOW_TYPE
            available_products = get_available_pioneer_products()

        return FlowProductRead(
            flow_type=flow_type,
            available_products=available_products,
        )

    except HTTPException:
        logger.exception('Ошибка в работе сервиса данных.')
        raise
