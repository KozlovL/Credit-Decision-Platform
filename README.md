# Shift Project

## Автор

**Козлов Леонид**
[GitHub](https://github.com/KozlovL)

---

## Описание проекта

Проект состоит из нескольких сервисов:

* **user-data-service** — сервис для хранения и управления данными пользователей.
* **flow-selection-service** — сервис выбора подходящего флоу для пользователя (pioneer/repeater).
* **scoring-service** — сервис скоринга пользователей и подбора подходящего продукта.
* **common** — общая директория с сущностями, схемами и константами, используемыми во всех сервисах.

Сервисы общаются между собой через REST API, а для асинхронной передачи событий используется Kafka.

---

## Docker и Kafka UI

Для локальной разработки проект использует Docker:

* **Kafka UI** доступен по адресу `http://localhost:8085` после запуска контейнеров.
* Основные сервисы в Docker:

  * Kafka: `kafka:29092`
  * Zookeeper: `zookeeper:2181`
  * Kafka UI: `kafka-ui:8085`

---

## Установка и запуск сервисов

**Требования:**

* Docker и Docker Compose
* Python 3.12
* Poetry

### 1. Клонирование репозитория и переход в корень проекта

```bash
git clone -b shift-3850 git@shift.gitlab.yandexcloud.net:shift-python/y2025/homeworks/kozlov-l/shift_project.git
cd shift_project
```

### 2. Копирование .env файла

```bash
cp .env.example .env
```

> Теперь все сервисы будут использовать настройки из `.env`.

### 3. Запуск всех контейнеров

```bash
docker compose up -d
```

> Все сервисы запустятся в фоне, включая Kafka и Kafka UI.

### 4. Доступ к сервисам


#### user-data-service


* Документация: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

#### flow-selection-service


* Документация: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### scoring-service


* Документация: [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs)

---

## Примеры JSON payload

### user-data-service

#### Создание нового пользователя

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

#### Добавление записи в кредитную историю

```json
{
  "phone": "72222222222",
  "loan_entry": {
    "loan_id": "loan_72222222222_20251103123000",
    "product_name": "ConsumerLoan",
    "amount": 1000000,
    "issue_date": "2025-11-03",
    "term_days": 90,
    "status": "open",
    "close_date": null
  }
}
```

### flow-selection-service

#### Определение флоу пользователя

```json
{
  "phone": "72222222222"
}
```

**Пример ответа:**

```json
{
  "flow_type": "pioneer",
  "available_products": [
    {"name": "MicroLoan", "max_amount": 3000000, "term_days": 30, "interest_rate_daily": 2.0},
    {"name": "QuickMoney", "max_amount": 1500000, "term_days": 15, "interest_rate_daily": 2.5}
  ]
}
```

### scoring-service

#### Скоринг первичных пользователей

```json
{
  "user_data": {
    "phone": "72222222222",
    "age": 25,
    "monthly_income": 3000000,
    "employment_type": "full_time",
    "has_property": false
  },
  "products": [
    {"name": "MicroLoan", "max_amount": 3000000, "term_days": 30, "interest_rate_daily": 2.0}
  ]
}
```

#### Скоринг повторных пользователей

```json
{
  "phone": "72222222222",
  "products": [
    {"name": "LoyaltyLoan", "max_amount": 10000000, "term_days": 30, "interest_rate_daily": 2.0},
    {"name": "AdvantagePlus", "max_amount": 25000000, "term_days": 60, "interest_rate_daily": 1.8}
  ]
}
```

---

## Запуск тестов

```bash
docker compose exec {service-name} poetry run pytest -v
```

---

## Примечания

* Все суммы указаны в копейках.
* Для корректной работы сервисов необходимо, чтобы Docker-контейнеры Kafka и Kafka UI были запущены.
* Kafka UI доступен по адресу: [http://localhost:8085](http://localhost:8085)
* Все импорты внутри проекта настроены так, чтобы начинаться с `app`.
