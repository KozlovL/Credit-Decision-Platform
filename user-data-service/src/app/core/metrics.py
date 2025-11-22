from prometheus_client import Counter, Histogram


# Счётчик всех HTTP запросов (для rate и ошибок)
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status', 'service_name']
)

# Гистограмма длительности запросов (duration)
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'endpoint', 'service_name'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

def init_service_metrics(service_name: str, version: str = '1.0.0'):
    """Инициализация метрик при запуске сервиса (placeholder)."""
    pass

def shutdown_service_metrics():
    """Шатдаун метрик при остановке сервиса (placeholder)."""
    pass
