import asyncio
import json
import logging
from typing import Any

from aiokafka import (
    AIOKafkaConsumer,  # type: ignore[import-untyped]
    ConsumerRecord,
)
from aiokafka.errors import KafkaError  # type: ignore[import-untyped]
from common.schemas.user import ProfileWrite
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import KafkaConfig
from app.core.db import async_session
from app.repository.user_data import user_data_crud
from app.schemas.user_data import LoanCreate

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """Кафка консьюмер для data-service."""

    def __init__(self, kafka_config: KafkaConfig):
        self._kafka_config = kafka_config
        self._consumer = AIOKafkaConsumer(
            self._kafka_config.topic,
            bootstrap_servers=kafka_config.url,
            auto_offset_reset='earliest',
            session_timeout_ms=kafka_config.session_timeout_ms,
            enable_auto_commit=False,
        )
        self._retry_timeout = kafka_config.retry_timeout_ms / 1000
        self._consume_task: asyncio.Task[None] | None = None
        self._is_running = False

    async def start(self) -> None:
        await self._consumer.start()
        self._is_running = True
        self._consume_task = asyncio.create_task(self._consume_loop())
        if not await self.is_connected():
            self._reconnect_task = asyncio.create_task(self._reconnect())

    async def stop(self) -> None:
        self._is_running = False
        if self._consume_task:
            self._consume_task.cancel()
        await self._consumer.stop()

    async def is_connected(self) -> bool:
        try:
            await self._consumer._client.fetch_all_metadata()
            return True
        except KafkaError:
            logger.exception('Kafka недоступна')
            return False

    async def _consume_loop(self) -> None:
        while self._is_running:
            try:
                async for message in self._consumer:
                    await self._process_message(message)
                    await self._commit_offset()
            except KafkaError:
                logger.exception('Ошибка при чтении сообщения из Kafka')
                await asyncio.sleep(self._retry_timeout)

    async def _process_message(self, message: ConsumerRecord) -> None:
        try:
            data = json.loads(message.value)
        except json.JSONDecodeError:
            logger.exception('Не удалось декодировать сообщение')
            return

        # Версионирование
        if data.get('version') != 1:
            logger.warning(
                f'Пропущено сообщение с неизвестной версией: {data.get("version")}'
            )
            return

        event_type = data.get('event_type')
        phone = data.get('phone')

        try:
            async with async_session() as session:
                if event_type == 'pioneer_accepted':
                    await self._handle_pioneer(session, data)
                elif event_type == 'repeater_accepted':
                    await self._handle_repeater(session, data)
                else:
                    logger.warning(f'Неизвестный тип события: {event_type}')
        except Exception as exc:
            logger.exception(f'Ошибка обработки сообщения для {phone}: {exc}')
            # Не коммитим оффсет, чтобы попытаться повторно

    async def _handle_pioneer(
            self,
            session: AsyncSession,
            data: dict[str, Any]
        ) -> None:
        """Обработка события pioneer_accepted."""
        phone = data['phone']
        profile_data = data['profile']
        loan_entry_data = data['loan_entry']

        user_profile = ProfileWrite(**profile_data)
        loan_entry = LoanCreate(**loan_entry_data)

        # Проверяем существование пользователя
        user = await user_data_crud.get_user_data(session=session, phone=phone)
        if user:
            logger.warning(f'Пионер {phone} уже существует')
        else:
            user = await user_data_crud.create_user_profile(
                session=session,
                phone=phone,
                profile=user_profile,
            )
            logger.info(f'Создан новый пользователь {phone} (пионер)')


        # Добавляем новую запись
        await user_data_crud.create_credit_note(
            session=session,
            loan_data=loan_entry,
            user=user,
        )
        logger.info(f'Обработано pioneer_accepted для {phone}')

    async def _handle_repeater(
            self,
            session:
            AsyncSession,
            data: dict[str, Any]
        ) -> None:
        """Обработка события repeater_accepted."""
        phone = data['phone']
        loan_entry_data = data['loan_entry']

        loan_entry = LoanCreate(**loan_entry_data)

        user = await user_data_crud.get_user_data(session=session, phone=phone)
        if not user:
            logger.warning(f'Пользователь {phone} не найден, пропускаем')
            return

        # Идемпотентность: если loan_id уже есть — игнорируем
        if any(cn.loan_id == loan_entry.loan_id for cn in user.credit_notes):
            logger.info(
                f'Запись loan_id={loan_entry.loan_id} уже существует для {phone}'
            )
            return

        # Добавляем новую запись
        await user_data_crud.create_credit_note(
            session=session,
            loan_data=loan_entry,
            user=user,
        )
        logger.info(f'Обработано repeater_accepted для {phone}')

    async def _commit_offset(self) -> None:
        await self._consumer.commit()

    async def _reconnect(self) -> None:
        is_connected = False
        while not is_connected:
            await asyncio.sleep(1)
            try:
                await self._consumer.start()
                is_connected = await self.is_connected()
            except KafkaError:
                pass
        logger.info('Подключение восстановлено')
