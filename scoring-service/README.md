# Shift Project

## Автор
**Козлов Леонид**  
[GitHub](https://github.com/KozlovL)

---

## Сервис: scoring_service

### POST `/api/scoring/pioneer`

**Описание:**  
Процесс скоринга пользователя и подбор подходящего продукта для первичника.


**Request body (JSON):**
```json
{
  "user_data": {
    "phone": "79123456789",
    "age": 28,
    "monthly_income": 4500000,
    "employment_type": "full_time",
    "has_property": true
  },
  "products": [
    {
      "name": "MicroLoan",
      "max_amount": 3000000,
      "term_days": 30,
      "interest_rate_daily": 2.0
    },
    {
      "name": "QuickMoney",
      "max_amount": 1500000,
      "term_days": 15,
      "interest_rate_daily": 2.5
    },
    {
      "name": "ConsumerLoan",
      "max_amount": 50000000,
      "term_days": 90,
      "interest_rate_daily": 1.5
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
    "interest_rate_daily": 2.5
  }
}
```

---

### POST `/api/scoring/repeater`

**Описание:**  
Процесс скоринга пользователя и подбор подходящего продукта для повторника.  
Пользователь должен уже существовать в "БД".

**Request body (JSON):**
```json
{
  "phone": "79123456789",
  "products": [
    {
      "name": "LoyaltyLoan",
      "max_amount": 10000000,
      "term_days": 30,
      "interest_rate_daily": 2.0
    },
    {
      "name": "AdvantagePlus",
      "max_amount": 25000000,
      "term_days": 60,
      "interest_rate_daily": 1.8
    },
    {
      "name": "PrimeCredit",
      "max_amount": 50000000,
      "term_days": 120,
      "interest_rate_daily": 1.3
    }
  ]
}
```

**Пример ответа (200 OK):**
```json
{
  "decision": "accepted",
  "product": {
    "name": "AdvantagePlus",
    "max_amount": 25000000,
    "term_days": 60,
    "interest_rate_daily": 1.8
  }
}
```

---

## Инструкция по запуску

**Требования:**

- Python 3.12
- Poetry



### 1. Клонирование репозитория и переход в корневую директорию

```bash
git clone -d shift-3804-2 git@shift.gitlab.yandexcloud.net:shift-python/y2025/homeworks/kozlov-l/shift_project.git
cd shift_project
```

Перед запуском сервиса нужно запустить все контейнеры Docker.
```bash
docker compose up -d
```

---

### 2. Создание виртуального окружения через Poetry

```bash
poetry install --no-root --directory scoring-service
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
poetry run --directory scoring-service uvicorn app.service:app --port 8002
```

- Сервер будет доступен по адресу: `http://127.0.0.1:8002`  
- Эндпоинты `/api/scoring/pioneer` и `/api/scoring/repeater` готовы к тестированию.  
- Документация доступна по адресу: `http://127.0.0.1:8002/docs`

---

### 5. Запуск тестов

```bash
poetry run --directory scoring-service pytest -v
```

---

### 6. Kafka UI

Если запущены все контейнеры Docker (Kafka, Zookeeper, сервисы), можно использовать Kafka UI для мониторинга кластеров Kafka.

- Kafka UI доступен по адресу: [http://127.0.0.1:8085](http://127.0.0.1:8085)  
- Используется кластер с именем `local`, который подключается к Kafka на `kafka:29092`.

---

**Примечание:**  
- Все команды выполняются из корня проекта после клонирования.  
- Все импорты внутри проекта настроены так, чтобы начинаться с `app`.  
- Для корректной работы убедитесь, что PYTHONPATH установлен на папку `src`.
