# Shift Project

## Автор
**Козлов Леонид**  
[GitHub](https://github.com/KozlovL)

---

## Сервис: scoring_service

Эндпоинт для скоринга нового пользователя:

### POST `/api/scoring/pioneer`

**Описание:**  
Процесс скоринга пользователя и подбор подходящего продукта.

**Request body (JSON):**

```json
{
  "user_data": {
    "phone": "79123456789",
    "age": 28,
    "monthly_income": 45000,
    "employment_type": "full_time",
    "has_property": true
  },
  "products": [
    {
      "name": "MicroLoan",
      "max_amount": 3000000,
      "term_days": 30,
      "interest_rate_daily": "2.0"
    },
    {
      "name": "QuickMoney",
      "max_amount": 1500000,
      "term_days": 15,
      "interest_rate_daily": "2.5"
    },
    {
      "name": "ConsumerLoan",
      "max_amount": 50000000,
      "term_days": 90,
      "interest_rate_daily": "1.5"
    }
  ]
}
```

**Пример ответа (200 OK):**

```json
{
  "decision": "accepted",
  "product": {
    "name": "QuickMoney",
    "max_amount": 1500000,
    "term_days": 15,
    "interest_rate_daily": "2.5"
  }
}
```

**Curl пример:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/scoring/pioneer' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
"user_data": {
  "phone": "79123456789",
  "age": 28,
  "monthly_income": 45000,
  "employment_type": "full_time",
  "has_property": true
},
"products": [
  {"name": "MicroLoan","max_amount":3000000,"term_days":30,"interest_rate_daily":"2.0"},
  {"name": "QuickMoney","max_amount":1500000,"term_days":15,"interest_rate_daily":"2.5"},
  {"name": "ConsumerLoan","max_amount":50000000,"term_days":90,"interest_rate_daily":"1.5"}
]
}'
```

---

## Инструкция по запуску

**Требования:**

- Python 3.12
- Poetry

### 1. Клонирование репозитория и переход в корневую директорию

```bash
git clone -b shift-3473 git@shift.gitlab.yandexcloud.net:shift-python/y2025/homeworks/kozlov-l/shift_project.git
cd shift_project
```

---

### 2. Создание виртуального окружения через Poetry

```bash
poetry install --no-root --directory scoring_service
```

---

### 3. Установка PYTHONPATH

**Windows (PowerShell):**

```powershell
$Env:PYTHONPATH = "$(pwd)\scoring_service\src"
```

**Linux/macOS:**

```bash
export PYTHONPATH="$(pwd)/scoring_service/src"
```

---

### 4. Запуск сервиса

```bash
poetry run --directory scoring_service uvicorn app.service:app
```

- Сервер будет доступен по адресу: `http://127.0.0.1:8000`.
- Эндпоинт `/api/scoring/pioneer` готов к тестированию.
- Документация доступна по адресу: `http://127.0.0.1:8000/docs`.

---

### 5. Запуск тестов

```bash
poetry run --directory scoring_service pytest -v
```

---

**Примечание:**

- Все команды выполняются из корня проекта после клонирования.
- Все импорты внутри проекта настроены так, чтобы начинаться с `app` (например, `from app.api.router import main_router`).
- Для корректной работы убедитесь, что PYTHONPATH установлен на папку `src`.

