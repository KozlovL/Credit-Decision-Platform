import pytest
import redis
from fastapi import HTTPException, status

from app.logic.user import get_products


def test_get_products_from_cache(mock_redis_client, mock_data_client):
    """Если продукты есть в кэше — должны вернуться из Redis без запроса к сервису."""
    cached_data = {'products': ['A', 'B']}
    mock_redis_client.get_from_cache.return_value = cached_data

    result = get_products('pioneer', mock_data_client, mock_redis_client)

    assert result == cached_data
    mock_data_client.get_products.assert_not_called()
    mock_redis_client.set_to_cache.assert_not_called()


def test_get_products_from_service_when_cache_empty(mock_redis_client, mock_data_client):
    """Если в кэше нет данных — должны пойти в data-service и записать в Redis."""
    mock_redis_client.get_from_cache.return_value = None
    products_from_service = {'products': ['C', 'D']}
    mock_data_client.get_products.return_value = products_from_service

    result = get_products('pioneer', mock_data_client, mock_redis_client)

    assert result == products_from_service
    mock_data_client.get_products.assert_called_once_with(flow_type='pioneer')
    mock_redis_client.set_to_cache.assert_called_once_with(
        key='pioneer_products', value=products_from_service
    )


def test_get_products_redis_unavailable_on_read(mock_redis_client, mock_data_client):
    """Если Redis недоступен при чтении — должны обратиться к data-service."""
    mock_redis_client.get_from_cache.side_effect = redis.RedisError('Redis down')
    mock_data_client.get_products.return_value = {'products': ['E', 'F']}

    result = get_products('pioneer', mock_data_client, mock_redis_client)

    assert result == {'products': ['E', 'F']}
    mock_data_client.get_products.assert_called_once()
    mock_redis_client.set_to_cache.assert_called_once()


def test_get_products_redis_unavailable_on_write(mock_redis_client, mock_data_client):
    """Если Redis недоступен при записи — не должно падать."""
    mock_redis_client.get_from_cache.return_value = None
    mock_data_client.get_products.return_value = {'products': ['G']}
    mock_redis_client.set_to_cache.side_effect = redis.RedisError('Write error')

    result = get_products('repeater', mock_data_client, mock_redis_client)

    assert result == {'products': ['G']}
    mock_data_client.get_products.assert_called_once()


def test_get_products_data_service_error(mock_redis_client, mock_data_client):
    """Если data-service возвращает ошибку, пробрасывается HTTPException 502."""
    mock_redis_client.get_from_cache.return_value = None
    mock_data_client.get_products.side_effect = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Service down'
    )

    with pytest.raises(HTTPException) as exc:
        get_products('pioneer', mock_data_client, mock_redis_client)

    assert exc.value.status_code == status.HTTP_502_BAD_GATEWAY
    assert 'Ошибка обращения к data-service' in exc.value.detail
