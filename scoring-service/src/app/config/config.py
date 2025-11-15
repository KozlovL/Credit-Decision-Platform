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


class KafkaConfig(BaseModel):
    url: str
    session_timeout_ms: int
    retry_timeout_ms: int
    topic: str


class Config(BaseModel):
    data_service: DataServiceConfig
    kafka: KafkaConfig

    @classmethod
    def from_yaml(cls, file_path: Path | str) -> 'Config':
        """Загрузка и валидация конфигурации из YAML-файла."""
        try:
            config_raw = yaml.safe_load(
                Path(file_path).read_text(encoding='utf8')
            )
            return cls(**config_raw)
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f'Файл конфигурации не найден: {file_path}'
            ) from error
        except ValidationError as error:
            raise ValueError(f'Неверная структура данных: {error}') from error
