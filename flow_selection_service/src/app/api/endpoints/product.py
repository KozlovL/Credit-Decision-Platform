from fastapi import APIRouter

from app.constants import PIONEER_FLOW_TYPE, REPEATER_FLOW_TYPE
from app.repository.product import AVAILABLE_PRODUCT_LIST, CUSTOMERS_PHONES
from app.schemas.product import CustomerWrite, ProductListRead

router = APIRouter(prefix='/products', tags=['products'])


@router.post(
    '',
    response_model=ProductListRead,
    summary='Выбор флоу по номеру телефона',
)
def select_flow(
        customer: CustomerWrite,
) -> ProductListRead:
    if customer.phone in CUSTOMERS_PHONES:
        return ProductListRead(
            flow_type=REPEATER_FLOW_TYPE,
            available_products=[],
        )
    return ProductListRead(
        flow_type=PIONEER_FLOW_TYPE,
        available_products=AVAILABLE_PRODUCT_LIST,
    )
