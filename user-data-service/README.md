# Shift Project

## Автор

**Козлов Леонид**
[GitHub](https://github.com/KozlovL)

---

## Сервис: user-data-service


### GET `/api/products?flow_type=pioneer`

**Описание:** Получение списка продуктов с фильтрацией по типу клиента.


### PUT `/api/user_data`

**Описание:** Создание нового пользователя.

**Пример request body:**

```json
{
  "phone": "72222222222",
  "profile": {
    "age": 25,
    "monthly_income": 3000000,
    "employment_type": "full_time",
    "has_property": false
  }
}
```

### PUT `/api/user_data`

**Описание:** Обновление профиля пользователя, добавление или изменение записи в кредитной истории.

**Пример request body для обновления профиля:**

```json
{
  "phone": "72222222222",
  "profile": {
    "age": 35,
    "monthly_income": 5000000,
    "employment_type": "full_time",
    "has_property": true
  }
}
```

**Пример request body для добавления новой записи в кредитной истории:**

```json
{
  "phone": "72222222222",
  "loan_entry": {
    "loan_id": "loan_72222222222_20251103153045",
    "product_name": "ConsumerLoan",
    "amount": 1000000,
    "issue_date": "2025-11-03",
    "term_days": 90,
    "status": "open",
    "close_date": null
  }
}
```

**Пример request body для обновления существующей записи:**

```json
{
  "phone": "72222222222",
  "loan_entry": {
    "loan_id": "loan_72222222222_20251103153045",
    "status": "closed",
    "close_date": "2025-12-03"
  }
}
```

### GET `/api/user_data?phone=72222222222`

**Описание:** Получение данных о пользователе по номеру телефона.

---

## Инструкция по запуску

**Требования:**

* Python 3.12
* Poetry
* Docker

### 1. Клонирование репозитория и переход в корневую директорию

```bash
git clone -b shift-3804-2 git@shift.gitlab.yandexcloud.net:shift-python/y2025/homeworks/kozlov-l/shift_project.git
cd shift_project
```

Перед запуском сервиса нужно поднять контейнеры Docker:

```bash
docker compose up -d
```

### 2. Создание виртуального окружения через Poetry

```bash
poetry install --no-root --directory user-data-service
```

### 3. Установка PYTHONPATH

**Windows (PowerShell):**

```powershell
$Env:PYTHONPATH = "$(pwd)\user-data-service\src"
```

**Linux/macOS:**

```bash
export PYTHONPATH="$(pwd)/user-data-service/src"
```

### 4. Создание .env файла

```bash
cp user-data-service/.env.example user-data-service/.env
```

### 5. Выполнение миграций и заполнение БД данными продуктов

```bash
poetry run --directory user-data-service alembic upgrade head
```

```bash
poetry run --directory user-data-service python -m app.seed
```

### 6. Запуск сервиса

```bash
poetry run --directory user-data-service uvicorn app.service:app --port 8001
```

* Сервер доступен по адресу: `http://127.0.0.1:8001`
* Документация доступна по адресу: `http://127.0.0.1:8001/docs`

### 7. Запуск тестов

```bash
poetry run --directory user-data-service pytest -v
```

---

**Примечание:**

* Все команды выполняются из корня проекта после клонирования.
* Все импорты внутри проекта настроены так, чтобы начинаться с `app`.
* Все суммы указаны в копейках.
* Сервис является Consumer в Kafka. При запущенных контейнерах можно открыть kafka-ui по адресу: `http://127.0.0.1:8085`
