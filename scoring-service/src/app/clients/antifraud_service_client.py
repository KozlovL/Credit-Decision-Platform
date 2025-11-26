import time
from http import HTTPStatus
from typing import Any

import httpx
from fastapi import HTTPException
from httpx import Response

from app.config.config import Config
from app.constants import CONFIG_PATH


class AntifraudServiceClient:
    """HTTP-клиент для взаимодействия с сервисом антифрода."""

    def __init__(self, config: Config):
        self.base_url = config.antifraud_service.base_url.rstrip('/')
        self.timeout = config.antifraud_service.timeout
        self.max_attempts = config.antifraud_service.retries.max_attempts
        self.delay = config.antifraud_service.retries.delay

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
                status_code = exc.response.status_code
                detail = exc.response.text
                raise HTTPException(status_code=status_code, detail=detail) from exc

            except httpx.RequestError as exc:
                if attempt < self.max_attempts:
                    time.sleep(self.delay)
                else:
                    raise HTTPException(
                        status_code=HTTPStatus.BAD_GATEWAY,
                        detail=f'Ошибка при обращении к {url}: {exc}'
                    ) from exc

        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail='Неизвестная ошибка при запросе'
        )

    def check_pioneer(self, payload: dict[str, Any]) -> Any:
        """Проверка первичного пользователя на антифрод."""
        response = self._request('POST', 'api/antifraud/pioneer/check', json=payload)
        return response.json()

    def check_repeater(self, payload: dict[str, Any]) -> Any:
        """Проверка повторного пользователя на антифрод."""
        response = self._request('POST', 'api/antifraud/repeater/check', json=payload)
        return response.json()


def get_antifraud_service_client() -> AntifraudServiceClient:
    """Клиент антифрода для DI."""
    config = Config.from_yaml(CONFIG_PATH)
    return AntifraudServiceClient(config=config)
