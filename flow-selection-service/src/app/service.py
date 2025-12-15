from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.routers import main_router
from app.config.tracing import instrument_fastapi, instrument_httpx, setup_tracing
from app.middleware.metrics import metrics_middleware

app = FastAPI()

setup_tracing(service_name='flow-selection-service-lkozlov')

# автоматическая инструментализация FastAPI
instrument_fastapi(app)  # type: ignore[no-untyped-call]

# автоматическая инструментализация httpx клиентов
instrument_httpx()  # type: ignore[no-untyped-call]

# middleware для метрик
app.middleware('http')(
    lambda request, call_next: metrics_middleware(
        request, call_next, 'flow-selection-service-lkozlov'
    )
)

# endpoint /metrics для Prometheus
@app.get('/metrics')
def metrics():  # type: ignore[no-untyped-def]
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(main_router)
