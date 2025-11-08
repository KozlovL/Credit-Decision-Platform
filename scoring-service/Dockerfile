# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Устанавливаем системные зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY scoring-service/pyproject.toml scoring-service/poetry.lock ./

# Копируем общие модули
COPY common /common

# Устанавливаем зависимости без установки самого пакета
RUN poetry install --no-root

# Копируем исходники сервиса
COPY scoring-service/src ./src

# Run stage
FROM python:3.12-slim

WORKDIR /app

# Устанавливаем runtime-зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем Poetry и установленные зависимости из билд-стадии
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# Копируем исходники сервиса
COPY --from=builder /app/src ./src

# Переменные окружения
ENV PYTHONPATH=/app/src

# Экспонируем порт
EXPOSE 8002

# Команда запуска
CMD ["poetry", "run", "uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
