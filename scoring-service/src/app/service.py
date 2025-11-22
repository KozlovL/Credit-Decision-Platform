import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.routers import main_router
from app.config.config import Config
from app.config.tracing import instrument_fastapi, instrument_httpx, setup_tracing
from app.constants import CONFIG_PATH
from app.kafka.producer import KafkaProducer
from app.middleware.metrics import metrics_middleware


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
        lifespan=lifespan
    )

    setup_tracing(service_name='scoring-service-lkozlov')

    # автоматическая инструментализация FastAPI
    instrument_fastapi(application)  # type: ignore[no-untyped-call]

    # автоматическая инструментализация httpx клиентов
    instrument_httpx()  # type: ignore[no-untyped-call]

    # middleware для метрик
    application.middleware('http')(
        lambda request, call_next: metrics_middleware(
            request, call_next, 'scoring-service-lkozlov'
        )
    )

    # endpoint /metrics для Prometheus
    @application.get('/metrics')
    def metrics():  # type: ignore[no-untyped-def]
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    application.include_router(main_router)
    return application


app = create_application()
