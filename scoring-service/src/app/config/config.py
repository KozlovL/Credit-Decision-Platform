from pathlib import Path
import yaml
from pydantic import BaseModel, Field, ValidationError


class RetryConfig(BaseModel):
    max_attempts: int = Field(..., alias='max_attempts')
    delay: int = Field(..., alias='delay')


class DataServiceConfig(BaseModel):
    base_url: str = Field(..., alias='base_url')
    timeout: int = Field(..., alias='timeout')
    retries: RetryConfig


class Config(BaseModel):
    data_service: DataServiceConfig

    @classmethod
    def from_yaml(cls, file_path: Path | str) -> 'Config':
        """Загрузка и валидация конфигурации из YAML-файла."""
        try:
            config_raw = yaml.safe_load(
                Path(file_path).read_text(encoding='utf8')
            )
            return cls(**config_raw)
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл конфигурации не найден: {file_path}')
        except ValidationError as error:
            raise ValueError(f'Неверная структура данных: {error}')
