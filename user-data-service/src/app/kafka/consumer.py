import asyncio
import json
import logging
from typing import Any

from aiokafka import (  # type: ignore[import-untyped]
    AIOKafkaConsumer,
    ConsumerRecord,
)
from aiokafka.errors import KafkaError  # type: ignore[import-untyped]
from common.repository.user import (
    add_user,
    get_user_by_phone,
)
from common.schemas.user import UserDataPhoneWrite

from app.core.config import KafkaConfig
from app.repository.user_data import (
    create_existing_credit_note,
    get_credit_history,
)
from app.schemas.user_data import LoanCreate

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """Кафка консьюмер для data-service."""

    def __init__(self, kafka_config: KafkaConfig):
        self._kafka_config = kafka_config
        self._consumer = AIOKafkaConsumer(
            self._kafka_config.topic,
            bootstrap_servers=kafka_config.url,
            group_id='user-data-service',
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
                f'Пропущено сообщение с неизвестной версией:'
                f' {data.get("version")}'
            )
            return

        event_type = data.get('event_type')
        phone = data.get('phone')

        try:
            if event_type == 'pioneer_accepted':
                self._handle_pioneer(data)
            elif event_type == 'repeater_accepted':
                self._handle_repeater(data)
            else:
                logger.warning(f'Неизвестный тип события: {event_type}')
        except Exception as exc:
            logger.exception(f'Ошибка обработки сообщения для {phone}: {exc}')
            # Не коммитим оффсет, чтобы попытаться повторно

    def _handle_pioneer(self, data: dict[str, Any]) -> None:
        """Обработка события pioneer_accepted."""
        phone = data['phone']
        profile_data = data['profile']
        loan_entry_data = data['loan_entry']

        # Валидация через Pydantic
        user_data = UserDataPhoneWrite(phone=phone, **profile_data)
        loan_entry = LoanCreate(**loan_entry_data)

        # Пионер — новый пользователь, добавляем сразу
        user = get_user_by_phone(phone)
        if user:
            logger.warning(
                f'Пионер {phone} уже существует в системе, '
                f'возможно повторное сообщение'
                )
        else:
            user = add_user(user_data)
            logger.info(f'Создан новый пользователь {phone} (пионер)')

        # Кредитная история пока отсутствует
        history = get_credit_history(user)

        # Идемпотентность: если loan_id уже есть — игнорируем
        if any(entry.loan_id == loan_entry.loan_id for entry in history):
            logger.info(
                f'Запись loan_id={loan_entry.loan_id} '
                f'уже существует для {phone}'
                )
            return

        # Добавляем новую запись
        credit_note = create_existing_credit_note(loan_entry)
        user.add_existing_credit_note(credit_note)
        logger.info(f'Обработано pioneer_accepted для {phone}')

    def _handle_repeater(self, data: dict[str, Any]) -> None:
        """Обработка события repeater_accepted."""
        phone = data['phone']
        loan_entry_data = data['loan_entry']

        # Валидация через Pydantic
        loan_entry = LoanCreate(**loan_entry_data)

        # Получаем пользователя
        user = get_user_by_phone(phone)
        if not user:
            logger.warning(f'Пользователь {phone} не найден, пропускаем')
            return
        logger.info(
            f'Найден пользователь {phone} для обработки repeater_accepted'
            )

        # Получаем кредитную историю
        history = get_credit_history(user)

        # Идемпотентность: если loan_id уже есть — игнорируем
        if any(entry.loan_id == loan_entry.loan_id for entry in history):
            logger.info(
                f'Запись loan_id={loan_entry.loan_id} '
                f'уже существует для {phone}'
                )
            return

        # Добавляем новую запись
        credit_note = create_existing_credit_note(loan_entry)
        user.add_existing_credit_note(credit_note)
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
