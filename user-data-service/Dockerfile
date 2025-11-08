# Build stage
FROM python:3.12-slim AS builder

# Рабочая директория
WORKDIR /app

# Устанавливаем системные зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY user-data-service/pyproject.toml user-data-service/poetry.lock ./

# Копируем общие модули
COPY common /common

# Устанавливаем зависимости (без установки самого пакета сервиса)
RUN poetry install --no-root

# Копируем исходники и миграции
COPY user-data-service/src ./src
COPY user-data-service/alembic ./alembic
COPY user-data-service/alembic.ini ./

# Run stage
FROM python:3.12-slim

WORKDIR /app

# Устанавливаем только runtime-зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем Poetry и уже установленные зависимости из билд-стадии
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# Копируем исходники и миграции
COPY --from=builder /app/src ./src
COPY --from=builder /app/alembic ./alembic
COPY --from=builder /app/alembic.ini ./

# Переменные окружения
ENV PYTHONPATH=/app/src

# Экспонируем порт
EXPOSE 8001

# Команда запуска
CMD ["poetry", "run", "uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
