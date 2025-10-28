import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI

from app.api.routers import main_router
from app.config.config import Config
from app.constants import CONFIG_PATH
from app.kafka.producer import KafkaProducer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Запускает и останавливает приложение с Kafka."""
    logging.info('Starting up...')

    # Загружаем конфиг
    config = Config.from_yaml(CONFIG_PATH)

    # Инициализация KafkaProducer
    kafka_config = config.kafka

    state = cast(Any, app.state)
    state.producer = KafkaProducer(kafka_config)
    await state.producer.start()

    yield

    logging.info('Shutting down...')
    await state.producer.stop()


def create_application() -> FastAPI:
    """Создаёт FastAPI-приложение с lifespan и роутерами."""
    application = FastAPI(
        lifespan=lifespan,
        openapi_url='/kafka_producer/openapi.json',
        docs_url='/kafka_producer/docs',
    )
    application.include_router(main_router)
    return application


app = create_application()
