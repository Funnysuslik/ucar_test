# Incident Tracker API

Небольшой сервис учёта инцидентов на FastAPI.
Проект был собран по образу моего toy проекта (toy_project_wallet), и немного 'beautyfied' код.
Была использована небольшая помощь агентов в настройках алембика и нджинкса.

## Стек

- FastAPI + SQLModel
- PostgreSQL + Alembic
- Pytest
- Docker / Docker Compose
- nginx

## Подготовка окружения

1. Скопируйте переменные окружения и при необходимости отредактируйте:
   ```bash
   cp env.example .env
   ```
2. Запустите инфраструктуру:
   ```bash
   cd infra
   docker compose up --build
   ```
   Бэкенд будет доступен на http://localhost/api/v1,

### Локальный запуск без Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic -c app/alembic.ini upgrade head
uvicorn app.main:app --reload
```

## Тесты

```bash
pytest
```

## Эндпоинты

- `POST /api/v1/incidents` — создать инцидент
- `GET /api/v1/incidents` — получить список (поддерживается фильтр `?status=...`)
- `GET /api/v1/incidents/{id}` — получить конкретный инцидент
- `PATCH /api/v1/incidents/{id}/status` — обновить статус
- `GET /health` — healthcheck

Примеры тел запросов и ответов — в Swagger UI  — http://localhost/docs..
