import logging
from typing import Any

import redis
from fastapi import HTTPException
from starlette import status

from app.clients.data_service_client import DataServiceClient
from app.clients.redis_client import RedisClient
from app.constants import PRODUCTS_KEY

logger = logging.getLogger(__name__)

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
        logger.error('Ошибка в работе сервиса данных.')
        # В остальных случаях возвращаем ошибку 502
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f'Ошибка обращения к user-data-service: {error.detail}'
        ) from error

def get_products(
    flow_type: str,
    client: DataServiceClient,
    redis_client: RedisClient,
) -> dict[str, Any]:
    """Получение списка продуктов с использованием Redis-кэша."""

    products = None
    key = f'{flow_type}_{PRODUCTS_KEY}'

    # Пытаемся взять из кэша
    try:
        products = redis_client.get_from_cache(key=key)
        if products is not None:
            return products
    except redis.RedisError as err:
        logger.warning(f'Redis недоступен: {err}')

    # Если в кэше нет — берём из сервиса данных
    try:
        products = client.get_products(flow_type=flow_type)
    except HTTPException as err:
        logger.error(f'Ошибка при обращении к data-service: {err.detail}')
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f'Ошибка обращения к data-service: {err.detail}',
        ) from err

    # Пишем в кэш
    try:
        redis_client.set_to_cache(key=key, value=products)
    except redis.RedisError as err:
        logger.warning(f'Ошибка записи в Redis: {err}')

    return products
