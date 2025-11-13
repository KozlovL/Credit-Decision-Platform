# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Виртуальное окружение в проекте
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# Файлы зависимостей сервиса
COPY flow-selection-service/pyproject.toml flow-selection-service/poetry.lock ./

# Копируем общие модули
COPY common /common

# Устанавливаем зависимости без установки самого пакета
RUN poetry install --no-root

# Исходники сервиса
COPY flow-selection-service/src ./src

# Run stage
FROM python:3.12-slim

WORKDIR /app

# Runtime-зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем .venv и Poetry из билд-стейджа
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# Копируем common
COPY --from=builder /common /common

# Копируем исходники
COPY --from=builder /app/src ./src

# Переменные окружения
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/src:/common

EXPOSE 8000

CMD ["uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "8000"]
