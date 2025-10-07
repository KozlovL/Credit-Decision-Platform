from common.repository.product import AVAILABLE_PRODUCT_LIST
from common.repository.user import USERS_PHONES, add_user
from common.schemas.user import UserPhoneWrite
from fastapi import APIRouter

from app.constants import (
    PIONEER_FLOW_TYPE,
    PRODUCT_PREFIX,
    PRODUCTS_TAG,
    REPEATER_FLOW_TYPE,
)
from app.schemas.product import FlowProductListRead

router = APIRouter(prefix=PRODUCT_PREFIX, tags=[PRODUCTS_TAG])


@router.post(
    '',
    response_model=FlowProductListRead,
    summary='Выбор флоу по номеру телефона',
)
def select_flow(
        user: UserPhoneWrite,
) -> FlowProductListRead:
    if user.phone in USERS_PHONES:
        return FlowProductListRead(
            flow_type=REPEATER_FLOW_TYPE,
            available_products=[],
        )
    # Записываем нового пользователя в "БД"
    add_user(user.phone)
    return FlowProductListRead(
        flow_type=PIONEER_FLOW_TYPE,
        available_products=AVAILABLE_PRODUCT_LIST,
    )
