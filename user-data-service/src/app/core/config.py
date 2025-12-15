import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from app.constants import CONFIG_PATH

load_dotenv()

class KafkaConfig(BaseModel):
    """Конфиг Kafka."""
    url: str
    session_timeout_ms: int
    retry_timeout_ms: int
    topic: str


class Config(BaseSettings):
    """Конфиг приложения, берущий все значения из YAML."""

    database_url: str = (
        f'postgresql+asyncpg://'
        f'{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}'
        f'@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
        f'/{os.getenv("POSTGRES_DB")}'
    )

    kafka: KafkaConfig | None = None

    @classmethod
    def load_kafka_from_yaml(cls, path: str | Path) -> KafkaConfig:
        """Загружает только Kafka-конфиг из YAML."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f'Файл не найден: {path}')

        with path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        kafka_cfg = data.get('kafka', {})

        bootstrap = kafka_cfg.get('bootstrap_servers', 'localhost:9092')
        host, port = bootstrap.split(':')

        return KafkaConfig(
            url=f'{host}:{port}',
            session_timeout_ms=kafka_cfg.get('session_timeout_ms', 10000),
            retry_timeout_ms=kafka_cfg.get('retry_timeout_ms', 2000),
            topic=kafka_cfg.get('topic', 'test_topic')
        )


# создаём объект Config с database_url из .env
config = Config()

# подгружаем Kafka из YAML отдельно
config.kafka = Config.load_kafka_from_yaml(CONFIG_PATH)
