# Credit Decision Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Poetry](https://img.shields.io/badge/Poetry-1.7+-purple.svg)](https://python-poetry.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io/)
[![Kafka](https://img.shields.io/badge/Kafka-3.4+-black.svg)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-24+-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-blue.svg)](https://kubernetes.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

---

## 📖 Оглавление

- [Описание проекта](#описание-проекта)
- [Ключевые возможности](#ключевые-возможности)
- [Архитектура](#архитектура)
- [Бизнес-процессы](#бизнес-процессы)
- [Технологический стек](#технологический-стек)
- [Структура проекта](#структура-проекта)
- [Быстрый старт](#быстрый-старт)
- [API-эндпоинты](#api-эндпоинты)
- [Примеры запросов](#примеры-запросов)
- [Тестирование](#тестирование)
- [Качество кода](#качество-кода)
- [Развёртывание](#развёртывание)
- [Примечания](#примечания)

---

## Описание проекта

**Credit Decision Platform** — это микросервисная платформа для автоматизации процессов принятия кредитных решений в финансовых организациях. Система обеспечивает полный цикл обработки заявки: от определения сценария обслуживания клиента до скоринговой оценки и антифрод-проверок.

Проект состоит из четырёх независимых сервисов, взаимодействующих через REST API и Apache Kafka:

| Сервис | Порт | Назначение |
|--------|------|------------|
| **user-data-service** | 8001 | Хранение и управление данными пользователей и кредитной историей |
| **flow-selection-service** | 8000 | Определение сценария обработки (PIONEER / REPEATER) |
| **scoring-service** | 8002 | Скоринг пользователей и подбор кредитного продукта |
| **antifraud-service** | 8003 | Антифрод-проверки по бизнес-правилам |

---

## Ключевые возможности

- ✅ **Управление данными клиентов** — централизованное хранение профилей пользователей и их кредитной истории (PostgreSQL)
- ✅ **Выбор сценария обслуживания** — автоматическое определение категории клиента (PIONEER / REPEATER) на основе кредитной истории
- ✅ **Скоринговая оценка** — расчёт кредитоспособности по балльной системе (макс. 17 баллов) с подбором оптимального продукта
- ✅ **Антифрод-проверки** — детерминированные проверки бизнес-правил для выявления мошеннических заявок (без ML)
- ✅ **Асинхронное взаимодействие** — передача событий между сервисами через Apache Kafka
- ✅ **Кэширование** — ускорение ответов и снижение нагрузки на БД с помощью Redis (TTL 5 минут)
- ✅ **Наблюдаемость** — мониторинг метрик (Prometheus), распределённый трейсинг (Jaeger) и визуализация (Grafana)
- ✅ **Контейнеризация и оркестрация** — Docker + Kubernetes с Helm-чартами
- ✅ **Качество кода** — Ruff (линтер), Black (форматирование), mypy (типизация), pytest (тесты)

---

## Архитектура

### Общая схема взаимодействия

![alt text](image.png)

### Поток данных (Kafka)

![alt text](mermaid-diagram-2026-06-19-182050.png)

### Схема развёртывания

![alt text](mermaid-diagram-2026-06-19-182211.png)

![alt text](mermaid-diagram-2026-06-19-182229.png)

## Бизнес-процессы

### Скоринговая модель

![alt text](mermaid-diagram-2026-06-19-182302.png)

### Факторы скоринга

![alt text](mermaid-diagram-2026-06-19-182348.png)

### Антифрод-проверки

![alt text](mermaid-diagram-2026-06-19-182411.png)

## Технологический стек

![alt text](mermaid-diagram-2026-06-19-182449.png)

## Структура проекта

```
Credit-Decision-Platform/
│
├── common/                              # Общая библиотека для всех сервисов
│   └── src/common/
│       ├── constants.py                 # Константы и перечисления
│       └── schemas/                     # Pydantic-модели
│
├── user-data-service/                   # Сервис управления данными (порт 8001)
│   ├── src/app/
│   │   ├── api/endpoints/               # REST API
│   │   ├── core/                        # Конфигурация, БД, миграции
│   │   ├── models/                      # SQLAlchemy-модели
│   │   ├── repository/                  # CRUD-операции
│   │   ├── kafka/                       # Kafka-консюмер
│   │   └── fixtures/                    # Начальные данные
│   ├── tests/                           # Модульные и интеграционные тесты
│   ├── charts/                          # Helm-чарт для Kubernetes
│   ├── manifests/                       # Манифесты Kubernetes
│   ├── alembic/                         # Миграции БД
│   ├── Dockerfile
│   └── pyproject.toml
│
├── flow-selection-service/              # Сервис выбора флоу (порт 8000)
│   ├── src/app/
│   │   ├── api/endpoints/               # REST API
│   │   ├── clients/                     # Клиенты (Data Service, Redis)
│   │   ├── logic/                       # Логика определения PIONEER/REPEATER
│   │   ├── repository/                  # Доступ к данным
│   │   └── fixtures/                    # JSON-файлы с продуктами
│   ├── tests/
│   ├── charts/
│   ├── manifests/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── scoring-service/                     # Сервис скоринга (порт 8002)
│   ├── src/app/
│   │   ├── api/endpoints/               # REST API
│   │   ├── clients/                     # Клиенты (Data Service, Antifraud)
│   │   ├── logic/                       # Алгоритмы скоринга
│   │   ├── kafka/                       # Kafka-продюсер
│   │   └── api/validators/              # Валидаторы
│   ├── tests/                           # Тесты для PIONEER и REPEATER
│   ├── charts/
│   ├── manifests/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── antifraud-service/                   # Сервис антифрода (порт 8003)
│   ├── src/app/
│   │   ├── api/endpoints/               # REST API
│   │   ├── clients/                     # Клиенты (Data Service, Redis)
│   │   ├── logic/                       # Бизнес-правила антифрода
│   │   └── schemas/                     # Pydantic-схемы
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── docker-compose.yml                   # Локальный запуск всех сервисов
├── .env.example                         # Шаблон переменных окружения
├── .gitlab-ci.yml                       # CI/CD пайплайн
├── pyproject.toml                       # Корневой Poetry-файл
├── README.md
└── CONTRIBUTING.md
```

## Быстрый старт

**Требования**
* Docker и Docker Compose

* Python 3.12+

* Poetry (опционально, для локальной разработки)

**Установка и запуск**

```bash
# 1. Клонирование репозитория
git clone https://github.com/KozlovL/Credit-Decision-Platform.git
cd Credit-Decision-Platform

# 2. Копирование .env файла
cp .env.example .env

# 3. Запуск всех сервисов в Docker
docker compose up -d

# 4. Проверка статуса контейнеров
docker compose ps
```

**Доступ к сервисам**

| Сервис                  | URL                                          |
|-------------------------|----------------------------------------------|
| user-data-service       | http://127.0.0.1:8001/docs                   |
| flow-selection-service  | http://127.0.0.1:8000/docs                   |
| scoring-service         | http://127.0.0.1:8002/docs                   |
| antifraud-service       | http://127.0.0.1:8003/docs                   |
| Kafka UI                | http://localhost:8085                        |

## API-эндпоинты

![alt text](mermaid-diagram-2026-06-19-183135.png)

## Примеры запросовПримеры запросов

**user-data-service — создание пользователя**

```
POST /api/user-data
{
  "phone": "72222222222",
  "profile": {
    "age": 25,
    "monthly_income": 3000000,
    "employment_type": "full_time",
    "has_property": false
  },
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
---
**flow-selection-service — определение флоу**
```
POST /api/product
{
  "phone": "72222222222"
}
```
**Ответ:**
```
{
  "flow_type": "repeater",
  "available_products": [
    {
      "name": "ConsumerLoan",
      "max_amount": 10000000,
      "term_days": 90,
      "interest_rate_daily": 1.5
    }
  ]
}
```
---
**scoring-service — скоринг PIONEER**
```
POST /api/scoring/pioneer
{
  "user_data": {
    "phone": "72222222221",
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
**Ответ:**
```
{
  "decision": "accepted",
  "product": {
    "name": "MicroLoan",
    "max_amount": 3000000,
    "term_days": 30,
    "interest_rate_daily": 2.0
  }
}
```
---
**antifraud-service — проверка PIONEER**
```POST /api/antifraud/pioneer/check
{
  "user_data": {
    "phone": "72222222221",
    "age": 28,
    "monthly_income": 4500000,
    "employment_type": "full_time",
    "has_property": true
  }
}
```
**Ответ (пройдена):**
```
{
  "decision": "passed",
  "reasons": []
}
```
**Ответ (не пройдена):**
```
{
  "decision": "rejected",
  "reasons": [
    "Минимальный возраст: 16 < 18",
    "Недостаточный доход: 15000 < 30000"
  ]
}
```
## Тестирование
**Запуск тестов**
```
# Все тесты для конкретного сервиса
docker compose exec {service-name} poetry run pytest -v

# Пример: все тесты для scoring-service
docker compose exec scoring-service poetry run pytest -v

# Тесты с покрытием
docker compose exec {service-name} poetry run pytest --cov=app --cov-report=term

# Все тесты для всех сервисов
for service in user-data-service flow-selection-service scoring-service antifraud-service; do
  docker compose exec $service poetry run pytest -v
done
```
В интеграционных тестах внешние вызовы к Data Service и Antifraud Service замоканы.

## Качество кода
**Инструменты**
| Инструмент | Назначение | Команда |
|------------|------------|---------|
| Ruff | Линтер и проверка стиля | `poetry run ruff check .` |
| mypy | Статическая проверка типов | `poetry run mypy .` |
| pytest | Модульное и интеграционное тестирование | `poetry run pytest -v` |
| pytest-cov | Проверка покрытия кода | `poetry run pytest --cov=app` |

**Проверка качества локально**
```

# Проверка стиля и линтинг
poetry run ruff check .

# Статическая проверка типов
poetry run mypy .

# Запуск всех тестов
poetry run pytest -v

# Проверка покрытия
poetry run pytest --cov=app --cov-report=term
```

## Развёртывание

**Helm-чарты**
Каждый сервис имеет собственный Helm-чарт в директории charts/.

```
# Применение всех чартов
helm install lkozlov-user-data-service user-data-service/charts -n test
helm install lkozlov-flow-selection-service flow-selection-service/charts -n test
helm install lkozlov-scoring-service scoring-service/charts -n test

# Проброс портов для локального доступа
kubectl port-forward svc/user-data-service-lkozlov 8081:8001 &
kubectl port-forward svc/flow-selection-service-lkozlov 8080:8000 &
kubectl port-forward svc/scoring-service-lkozlov 8082:8002 &

# Обновление чарта
helm upgrade lkozlov-user-data-service user-data-service/charts -n test

# Удаление релиза
helm uninstall lkozlov-user-data-service -n test
```

## Мониторинг

**Метрики, собираемые с каждого сервиса:**

* Количество HTTP-запросов

* Время ответа (latency)

* Количество ошибок (5xx, 4xx)

* Количество успешных/отклонённых скорингов

* Количество антифрод-проверок

## Примечания

**Важные особенности**
* Все суммы указаны в копейках — это позволяет избежать ошибок округления при финансовых расчётах.

* Номер телефона используется как уникальный идентификатор пользователя.

* Отказоустойчивость — при недоступности Data Service или Redis сервисы возвращают ошибку 502 Bad Gateway.

* Идемпотентность — повторные события Kafka не создают дублирующих записей в БД.

* Версионирование событий — поле version в сообщениях Kafka обеспечивает обратную совместимость.

* Развертывание через Helm доступно только через сервер