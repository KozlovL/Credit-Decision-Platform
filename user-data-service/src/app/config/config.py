from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class KafkaConfig(BaseModel):
    """Конфиг Kafka."""
    url: str
    session_timeout_ms: int
    retry_timeout_ms: int
    topic: str


class Config(BaseSettings):
    """Конфиг приложения, берущий все значения из YAML."""

    kafka: KafkaConfig

    @classmethod
    def from_yaml(cls, path: str | Path) -> 'Config':
        """Загружает конфиг из YAML-файла."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f'Файл не найден: {path}')

        with path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        kafka_cfg = data.get('kafka', {})

        # Разбираем bootstrap_servers на host:port
        bootstrap = kafka_cfg.get('bootstrap_servers', 'localhost:9092')
        host, port = bootstrap.split(':')

        kafka = KafkaConfig(
            url=f'{host}:{port}',
            session_timeout_ms=kafka_cfg.get('session_timeout_ms', 10000),
            retry_timeout_ms=kafka_cfg.get('retry_timeout_ms', 2000),
            topic=kafka_cfg.get('topic', 'test_topic')
        )

        return cls(kafka=kafka)
