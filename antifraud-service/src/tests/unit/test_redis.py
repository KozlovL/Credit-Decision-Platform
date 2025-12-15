from fastapi import HTTPException
import pytest
import redis
from app.constants import MAX_APPLICATIONS_PER_DAY
from starlette import status

@pytest.mark.asyncio
async def test_daily_limit_ok(antifraud, mock_redis_client):
    """Тест на валидное количество заявок в сутки."""
    mock_redis_client.get_events.return_value = [1, 2]  # меньше лимита
    antifraud.redis = mock_redis_client

    await antifraud.check_daily_application_limit()

    mock_redis_client.get_events.assert_awaited_once()
    mock_redis_client.add_event_zset.assert_awaited_once()
    assert antifraud.reasons == []


@pytest.mark.asyncio
async def test_daily_limit_exceeded(antifraud, mock_redis_client):
    """Тест на превышение лимита заявок за день."""
    mock_redis_client.get_events.return_value = list(range(MAX_APPLICATIONS_PER_DAY))
    antifraud.redis = mock_redis_client

    await antifraud.check_daily_application_limit()

    assert len(antifraud.reasons) == 1
    assert 'Daily application limit' in antifraud.reasons[0]
    mock_redis_client.add_event_zset.assert_awaited_once()


@pytest.mark.asyncio
async def test_daily_limit_redis_error(antifraud, mock_redis_client):
    """Тест на возврат 502 при ошибке в работе Redis."""
    mock_redis_client.get_events.side_effect = redis.RedisError()
    antifraud.redis = mock_redis_client

    with pytest.raises(HTTPException) as exc:
        await antifraud.check_daily_application_limit()

    assert exc.value.status_code == status.HTTP_502_BAD_GATEWAY
