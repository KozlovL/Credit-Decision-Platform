import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI

from app.api.routers import main_router
from app.config.config import Config
from app.constants import CONFIG_PATH
from app.kafka.consumer import KafkaConsumer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Запускает и останавливает приложение с Kafka consumer."""
    logging.info('Starting up user-data-service...')

    # Загружаем конфиг
    config = Config.from_yaml(CONFIG_PATH)

    # Инициализация KafkaConsumer
    kafka_config = config.kafka
    state = cast(Any, app.state)
    state.consumer = KafkaConsumer(kafka_config)
    await state.consumer.start()

    yield

    logging.info('Shutting down user-data-service...')
    await state.consumer.stop()


def create_application() -> FastAPI:
    """Создает FastAPI-приложение с lifespan и роутерами."""
    application = FastAPI(
        lifespan=lifespan,
        openapi_url='/user-data-service/openapi.json',
        docs_url='/user-data-service/docs',
    )
    application.include_router(main_router)
    return application


app = create_application()
