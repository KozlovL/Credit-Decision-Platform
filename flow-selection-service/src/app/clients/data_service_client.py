import time
from http import HTTPStatus
from typing import Any

import httpx
from fastapi import HTTPException
from httpx import Response

from app.config.config import Config, config


class DataServiceClient:
    """HTTP-клиент для взаимодействия с data-service."""

    def __init__(self, config: Config):
        self.base_url = config.data_service.base_url.rstrip('/')
        self.timeout = config.data_service.timeout
        self.max_attempts = config.data_service.retries.max_attempts
        self.delay = config.data_service.retries.delay

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        """Выполнение HTTP-запроса с поддержкой ретраев."""
        url = f'{self.base_url}/{endpoint.lstrip("/")}'

        for attempt in range(1, self.max_attempts + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.request(method, url, **kwargs)
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as exc:
                # HTTP ошибка сервиса — пробрасываем FastAPI HTTPException
                status_code = exc.response.status_code
                detail = exc.response.text
                raise HTTPException(
                    status_code=status_code, detail=detail
                    ) from exc

            except httpx.RequestError as exc:
                if attempt < self.max_attempts:
                    time.sleep(self.delay)
                else:
                    # При исчерпании ретраев пробрасываем 502
                    raise HTTPException(
                        status_code=HTTPStatus.BAD_GATEWAY,
                        detail=f'Ошибка при обращении к {url}: {exc}'
                    ) from exc

        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail='Неизвестная ошибка при запросе'
        )

    def get_user_data(self, phone: str) -> Any:
        """Получение данных пользователя по номеру телефона."""
        response = self._request('GET', f'api/user-data?phone={phone}')
        return response.json()

    def put_user_data(self, payload: dict[str, Any]) -> Any:
        """Создание или обновление данных пользователя."""
        response = self._request('PUT', 'api/user-data', json=payload)
        return response.json()
    
    def get_products(self, flow_type: str | None) -> Any:
        """Получение списка продуктов."""
        response = self._request('GET', f'api/products?flow_type={flow_type}')
        return response.json()


def get_data_service_client() -> DataServiceClient:
    """Клиент для DI."""
    return DataServiceClient(config=config)
