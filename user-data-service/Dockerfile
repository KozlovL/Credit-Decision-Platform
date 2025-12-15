# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Создаём виртуальное окружение в проекте
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# Копируем файлы зависимостей
COPY user-data-service/pyproject.toml user-data-service/poetry.lock ./

# Копируем общие модули
COPY common /common

# Устанавливаем зависимости (без установки самого пакета)
RUN poetry install --no-root

# Копируем исходники и миграции
COPY user-data-service/src ./src
COPY user-data-service/alembic ./alembic
COPY user-data-service/alembic.ini ./

# Run stage
FROM python:3.12-slim

WORKDIR /app

# Только runtime-зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем .venv и Poetry из билд-стейджа
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# Копируем common
COPY --from=builder /common /common

# Копируем исходники и миграции
COPY --from=builder /app/src ./src
COPY --from=builder /app/alembic ./alembic
COPY --from=builder /app/alembic.ini ./

# Используем виртуальное окружение
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/src

EXPOSE 8001

CMD ["bash", "-c", "alembic upgrade head && python -m app.seed && uvicorn app.service:app --host 0.0.0.0 --port 8001"]
