# Shift Project

## Автор
**Козлов Леонид**  
[GitHub](https://github.com/KozlovL)

---

## Сервис: flow_selection_service

Эндпоинт для выбора флоу по номеру телефона:

### POST `/api/products`

**Описание:**  
Выбор флоу (новый/существующий клиент) по номеру телефона.

**Request body (JSON):**

```json
{
  "phone": "71111112111"
}
```

**Пример ответа (200 OK):**

```json
{
  "flow_type": "pioneer",
  "available_products": [
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

**Curl пример:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/products' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
"phone": "71111112111"
}'
```

---

## Инструкция по запуску

**Требования:**

- Python 3.12
- Poetry

### 1. Клонирование репозитория и переход в корневую директорию

```bash
git clone -b shift-3428 git@shift.gitlab.yandexcloud.net:L_K/shift_project.git
cd shift_project
```

---

### 2. Создание виртуального окружения через Poetry

```bash
poetry install --no-root --directory flow_selection_service
```

---

### 3. Установка PYTHONPATH

**Windows (PowerShell):**

```powershell
$Env:PYTHONPATH = "$(pwd)\flow_selection_service\src"
```

**Linux/macOS:**

```bash
export PYTHONPATH="$(pwd)/flow_selection_service/src"
```

---

### 4. Запуск сервиса

```bash
poetry run --directory flow_selection_service uvicorn app.service:app
```

- Сервер будет доступен по адресу: `http://127.0.0.1:8000`.
- Эндпоинт `/api/products` готов к тестированию.
- Документация доступна по адресу: `http://127.0.0.1:8000/docs`.

---

### 5. Запуск тестов

```bash
poetry run --directory flow_selection_service pytest -v
```

---

💡 **Примечание:**

- Все команды выполняются из корня проекта после клонирования.
- Все импорты внутри проекта настроены так, чтобы начинаться с `app` (например, `from app.api.router import main_router`).
- Для корректной работы убедитесь, что PYTHONPATH установлен на папку `src`.

