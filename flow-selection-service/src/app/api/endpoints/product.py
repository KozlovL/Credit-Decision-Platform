from common.constants import ClientType
from common.schemas.user import UserPhoneWrite
from fastapi import APIRouter, Depends

from app.clients.data_service_client import DataServiceClient, get_data_service_client
from app.clients.redis_client import RedisClient, get_redis_client
from app.constants import PRODUCT_PREFIX, PRODUCTS_TAG
from app.logic.user import get_products, is_repeater
from app.schemas.product import FlowProductRead

router = APIRouter(prefix=PRODUCT_PREFIX, tags=[PRODUCTS_TAG])


@router.post(
    '',
    response_model=FlowProductRead,
    summary='Выбор флоу по номеру телефона',
)
def select_flow(
        user: UserPhoneWrite,
        client: DataServiceClient = Depends(get_data_service_client),
        redis_client: RedisClient = Depends(get_redis_client)
) -> FlowProductRead:

        # Если пользователь повторник...
        if is_repeater(phone=user.phone, client=client):
            flow_type = ClientType.REPEATER.value
            products = get_products(
                flow_type=flow_type,
                client=client,
                redis_client=redis_client
            )
        else:
            flow_type = ClientType.PIONEER.value
            products = get_products(
                flow_type=flow_type,
                client=client,
                redis_client=redis_client
            )

        return FlowProductRead(
            flow_type=flow_type,
            available_products=products,
        )
