import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor


logger = logging.getLogger(__name__)


def setup_tracing(service_name: str):
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


def instrument_fastapi(app):
    FastAPIInstrumentor().instrument_app(app)


def instrument_httpx():
    HTTPXClientInstrumentor().instrument()


def get_tracer():
    return trace.get_tracer(__name__)
