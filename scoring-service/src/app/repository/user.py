from datetime import UTC, datetime
from typing import Any

from common.constants import CreditStatus
from common.schemas.product import ProductWrite
from common.schemas.user import ProfileWrite

from app.clients.data_service_client import DataServiceClient
from app.logic.scoring_process import generate_loan_id


def put_profile_and_loan(
        phone: str,
        user_data: ProfileWrite,
        available_product: ProductWrite,
        client: DataServiceClient
) -> Any:
    """Функция PUT запроса к сервису данных с профилем и записью."""
    return client.put_user_data(
        payload={
            'phone': phone,
            'profile': {**user_data.model_dump()},
            'loan_entry': {
                'loan_id': generate_loan_id(phone=phone),
                'product_name': available_product.name,
                'amount': available_product.max_amount,
                'issue_date': str(datetime.now(UTC).date()),
                'term_days': available_product.term_days,
                'status': CreditStatus.OPEN,
                'close_date': None,
            }
        }
    )


def put_loan(
        phone: str,
        available_product: ProductWrite,
        client: DataServiceClient
) -> Any:
    """Функция PUT запроса к сервису данных с записью."""
    return client.put_user_data(
        payload={
            'phone': phone,
            'loan_entry': {
                'loan_id': generate_loan_id(phone=phone),
                'product_name': available_product.name,
                'amount': available_product.max_amount,
                'issue_date': str(datetime.now(UTC).date()),
                'term_days': available_product.term_days,
                'status': CreditStatus.OPEN,
                'close_date': None,
            }
        }
    )
