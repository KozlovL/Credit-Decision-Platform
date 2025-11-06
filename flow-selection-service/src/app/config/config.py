from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError
from app.constants import CONFIG_PATH


class RetryConfig(BaseModel):
    max_attempts: int = Field(..., alias='max_attempts')
    delay: int = Field(..., alias='delay')


class DataServiceConfig(BaseModel):
    base_url: str = Field(..., alias='base_url')
    timeout: int = Field(..., alias='timeout')
    retries: RetryConfig


class RedisConfig(BaseModel):
    host: str = Field(..., alias='host')
    port: int = Field(..., alias='port')
    db: int = Field(0, alias='db')
    ttl: int = Field(300, alias='ttl')


class Config(BaseModel):
    data_service: DataServiceConfig
    redis: RedisConfig

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


config = Config.from_yaml(CONFIG_PATH)
