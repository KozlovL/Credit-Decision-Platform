# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию для сервиса
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY user-data-service/pyproject.toml user-data-service/poetry.lock ./

# Копируем директорию common
COPY common /common

# Устанавливаем все зависимости
RUN poetry install --no-root

# Копируем исходники сервиса
COPY user-data-service/src ./src

# Копируем файлы миграций
COPY user-data-service/alembic  ./alembic

COPY user-data-service/alembic.ini  ./

# Переменные окружения
ENV PYTHONPATH=/app/src

# Экспонируем порт сервиса
EXPOSE 8001

# Команда запуска сервиса
CMD ["poetry", "run", "uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
