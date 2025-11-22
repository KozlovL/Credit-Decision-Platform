import logging
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)


def setup_tracing(service_name: str):  # type: ignore[no-untyped-def]
    # Default: OTEL Collector
    otlp_endpoint = os.getenv(
        'OTEL_EXPORTER_OTLP_ENDPOINT',
        'http://infra-jaeger-collector.infra.svc.cluster.local:4318'
    )

    provider = TracerProvider(
        resource=Resource(attributes={
            SERVICE_NAME: service_name
        })
    )

    exporter = OTLPSpanExporter(
        endpoint=f'{otlp_endpoint}/v1/traces'
    )

    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    logger.info(f'Tracing enabled → {otlp_endpoint}, service={service_name}')


def instrument_fastapi(app):  # type: ignore[no-untyped-def]
    FastAPIInstrumentor().instrument_app(app)


def instrument_httpx():  # type: ignore[no-untyped-def]
    HTTPXClientInstrumentor().instrument()


def get_tracer():  # type: ignore[no-untyped-def]
    return trace.get_tracer(__name__)
