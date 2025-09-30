from fastapi import APIRouter

from app.constants import REPEATER_FLOW_TYPE, PIONEER_FLOW_TYPE
from app.repository.product import AVAILABLE_PRODUCT_LIST, CUSTOMERS_PHONES
from app.schemas.product import ProductListRead, CustomerWrite

router = APIRouter(prefix='/products', tags=['products'])


@router.post(
    '',
    response_model=ProductListRead,
    summary='Выбор флоу по номеру телефона',
)
def select_flow(
        customer: CustomerWrite,
):
    if customer.phone in CUSTOMERS_PHONES:
        return {
            'flow_type': REPEATER_FLOW_TYPE,
            'available_products': []
        }
    return {
            'flow_type': PIONEER_FLOW_TYPE,
            'available_products': AVAILABLE_PRODUCT_LIST
        }
