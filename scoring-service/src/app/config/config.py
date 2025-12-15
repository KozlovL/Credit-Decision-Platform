from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError


class RetryConfig(BaseModel):
    max_attempts: int
    delay: int


class DataServiceConfig(BaseModel):
    base_url: str
    timeout: int
    retries: RetryConfig


class AntifraudServiceConfig(DataServiceConfig):
    pass


class KafkaConfig(BaseModel):
    url: str
    session_timeout_ms: int
    retry_timeout_ms: int
    topic: str


class Config(BaseModel):
    data_service: DataServiceConfig
    antifraud_service: AntifraudServiceConfig
    kafka: KafkaConfig

    @classmethod
    def from_yaml(cls, file_path: str | Path) -> 'Config':
        """Загружает и валидирует конфигурацию из YAML."""
        try:
            raw_data = yaml.safe_load(
                Path(file_path).read_text(encoding='utf-8')
            )

            # Разбираем Kafka bootstrap_servers на host:port
            kafka_raw = raw_data.get('kafka', {})
            bootstrap = kafka_raw.get('bootstrap_servers', 'localhost:9092')
            host, port = bootstrap.split(':')

            kafka = KafkaConfig(
                url=f'{host}:{port}',
                session_timeout_ms=kafka_raw.get('session_timeout_ms', 10000),
                retry_timeout_ms=kafka_raw.get('retry_timeout_ms', 2000),
                topic=kafka_raw.get('topic', 'test_topic')
            )

            # Разбираем data_service
            data_service_raw = raw_data.get('data_service', {})
            retries_raw = data_service_raw.get('retries', {})
            retries = RetryConfig(
                max_attempts=retries_raw.get('max_attempts', 3),
                delay=retries_raw.get('delay', 1)
            )
            data_service = DataServiceConfig(
                base_url=data_service_raw.get(
                    'base_url',
                    'http://localhost:8001'
                ),
                timeout=data_service_raw.get('timeout', 5),
                retries=retries
            )

            # Разбираем antifraud_service
            antifraud_service_raw = raw_data.get('antifraud_service', {})
            retries_raw = antifraud_service_raw.get('retries', {})
            retries = RetryConfig(
                max_attempts=retries_raw.get('max_attempts', 3),
                delay=retries_raw.get('delay', 1)
            )
            antifraud_service = AntifraudServiceConfig(
                base_url=antifraud_service_raw.get(
                    'base_url',
                    'http://localhost:8003'
                ),
                timeout=antifraud_service_raw.get('timeout', 5),
                retries=retries
            )

            return cls(
                data_service=data_service,
                kafka=kafka,
                antifraud_service=antifraud_service
            )

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f'Файл конфигурации не найден: {file_path}'
            ) from e
        except ValidationError as e:
            raise ValueError(f'Ошибка валидации конфигурации: {e}') from e
