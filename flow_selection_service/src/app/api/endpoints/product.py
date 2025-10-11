from common.repository.user import get_users
from common.schemas.product import ProductRead
from common.schemas.user import UserPhoneWrite
from fastapi import APIRouter

from app.constants import (
    PIONEER_FLOW_TYPE,
    PRODUCT_PREFIX,
    PRODUCTS_TAG,
    REPEATER_FLOW_TYPE,
)
from app.logic.user import is_repeater
from app.repository.products import (
    get_available_repeater_products,
    get_available_pioneer_products,
)
from app.schemas.product import FlowProductRead

router = APIRouter(prefix=PRODUCT_PREFIX, tags=[PRODUCTS_TAG])


@router.post(
    '',
    response_model=FlowProductRead,
    summary='Выбор флоу по номеру телефона',
)
def select_flow(
        user: UserPhoneWrite,
) -> FlowProductRead:

    # Если пользователь повторник...
    if is_repeater(phone=user.phone):
        # выводим данные для повторника, ...
        flow_type = REPEATER_FLOW_TYPE
        available_products = get_available_repeater_products()
    else:
        # иначе выводим данные для первичника
        flow_type = PIONEER_FLOW_TYPE
        available_products = get_available_pioneer_products()

    return FlowProductRead(
        flow_type=flow_type,
        available_products=available_products,
    )
