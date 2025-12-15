import asyncio
import json
import logging
from typing import Any

from aiokafka import AIOKafkaProducer  # type: ignore[import-untyped]
from aiokafka.errors import (  # type: ignore[import-untyped]
    KafkaConnectionError,
    KafkaError,
)

from app.config.config import KafkaConfig


class KafkaProducer:
    """Кафка продюсер."""

    def __init__(
        self,
        kafka_config: KafkaConfig,
    ):
        """Инициализация клиента."""
        self._kafka_config = kafka_config
        self._producer = AIOKafkaProducer(
            bootstrap_servers=kafka_config.url,
            request_timeout_ms=kafka_config.session_timeout_ms,
        )
        self._topic = self._kafka_config.topic

    async def start(self) -> None:
        """Запускает продюсер и подключается к Кафке."""
        await self._start()
        if not await self.is_connected():
            self._reconnect_task = asyncio.create_task(self._reconnect())

    async def stop(self) -> None:
        """Останавливает продюсер."""
        await self._producer.stop()

    async def send(
        self,
        message: dict[str, Any],
    ) -> None:
        """Отправляет сообщение в топиках."""
        message_data = json.dumps(message, default=str).encode('utf-8')
        key_bytes = str(message.get('phone')).encode('utf-8')
        try:
            await self._producer.send_and_wait(
                topic=self._topic,
                value=message_data,
                key=key_bytes,
            )
        except KafkaError:
            logging.exception('Не получилось отправить сообщение в Kafka')
            raise

        logging.info('Сообщение отправлено в Kafka')

    async def is_connected(self) -> bool:
        """Проверяет доступность кафки."""
        try:
            await self._producer.client.fetch_all_metadata()
        except KafkaError:
            logging.exception('Kafka недоступна')
        else:
            return True
        return False

    async def _start(self) -> None:
        """Запускает продюсер."""
        try:
            await self._producer.start()
        except KafkaConnectionError:
            logging.error('Не удается подключиться к Kafka')

    async def _reconnect(self) -> None:
        """Пытается переподключиться к Кафке."""
        is_connected = False
        while not is_connected:
            await asyncio.sleep(1)
            await self._start()
            is_connected = await self.is_connected()
        logging.info('Kafka подключена заново')
