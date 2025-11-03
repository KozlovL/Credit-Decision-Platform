# Changelog
Все заметные изменения этого проекта будут задокументированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и этот проект следует [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]
- 

## [0.1.0] - 2025-09-30
### Added
- Сервис выбора флоу: `flow-selection-service`

## [0.2.0] - 2025-10-07
### Added
- Сервис скоринга: `scoring-service`

## [0.3.0] - 2025-10-21
### Added
- Сервис данных: `user-data-service`

## [0.4.0] - 2025-10-24
### Added
- Интеграция `user-data-service` в `scoring-service` через HTTP REST API

## [0.5.0] - 2025-10-24
### Added
- Интеграция `user-data-service` в `flow-selection-service` через HTTP REST API

## [0.6.0] - 2025-10-26
### Added
- Асинхронная интеграция через Kafka между `user-data-service` и `scoring-service`

## [0.7.0] - 2025-11-03
### Added
- Персистентное хранилище PostgreSQL для `user-data-service`
