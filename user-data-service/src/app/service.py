import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.routers import main_router
from app.core.config import config
from app.kafka.consumer import KafkaConsumer
from app.middleware.metrics import metrics_middleware
from app.core.tracing import setup_tracing, instrument_fastapi, instrument_httpx


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Запускает и останавливает приложение с Kafka consumer."""
    logging.info('Starting up user-data-service...')

    # Инициализация KafkaConsumer
    kafka_config = config.kafka
    state = cast(Any, app.state)
    state.consumer = KafkaConsumer(kafka_config)  # type: ignore[arg-type]
    await state.consumer.start()

    yield

    logging.info('Shutting down user-data-service...')
    await state.consumer.stop()


def create_application() -> FastAPI:
    """Создает FastAPI-приложение с lifespan и роутерами."""
    application = FastAPI(
        lifespan=lifespan,
    )

    setup_tracing(service_name='user-data-service')

    # автоматическая инструментализация FastAPI
    instrument_fastapi(application)

    # автоматическая инструментализация httpx клиентов
    instrument_httpx()

    # middleware для метрик
    application.middleware('http')(
        lambda request, call_next: metrics_middleware(
            request, call_next, 'user-data-service'
        )
    )

    # endpoint /metrics для Prometheus
    @application.get('/metrics')
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    application.include_router(main_router)
    return application


app = create_application()
