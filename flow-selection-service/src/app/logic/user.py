from common.repository.user import get_users
from fastapi import HTTPException
from starlette import status

from app.clients.data_service_client import DataServiceClient


def is_repeater(phone: str, client: DataServiceClient) -> bool:
    """Проверяет через data-service, существует ли пользователь."""
    try:
        client.get_user_data(phone)
        # True, если пользователь повторник
        return True
    except HTTPException as error:
        if error.status_code == status.HTTP_404_NOT_FOUND:
            # False, если пользователь первичник
            return False
        # В остальных случаях возвращаем ошибку 502
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f'Ошибка обращения к user-data-service: {error.detail}'
        ) from error
