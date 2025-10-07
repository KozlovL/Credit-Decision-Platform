from common.repository.product import AVAILABLE_PRODUCT_LIST
from common.schemas.user import UserPhoneWrite
from fastapi import APIRouter

from app.constants import PIONEER_FLOW_TYPE, REPEATER_FLOW_TYPE
from app.repository.product import CUSTOMERS_PHONES, add_customer
from app.schemas.product import ProductListRead

router = APIRouter(prefix='/products', tags=['products'])


@router.post(
    '',
    response_model=ProductListRead,
    summary='Выбор флоу по номеру телефона',
)
def select_flow(
        customer: UserPhoneWrite,
) -> ProductListRead:
    if customer.phone in CUSTOMERS_PHONES:
        return ProductListRead(
            flow_type=REPEATER_FLOW_TYPE,
            available_products=[],
        )
    # Записываем нового пользователя в "БД"
    add_customer(customer.phone)
    return ProductListRead(
        flow_type=PIONEER_FLOW_TYPE,
        available_products=AVAILABLE_PRODUCT_LIST,
    )
