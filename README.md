# Mini Marketplace API

[![CI](https://github.com/balobol229-cmd/mini-marketplace/actions/workflows/ci.yml/badge.svg)](https://github.com/balobol229-cmd/mini-marketplace/actions/workflows/ci.yml)

Backend мини-маркетплейса на FastAPI. Пользователи регистрируются, выставляют товары на продажу и покупают товары друг у друга. Авторизация через JWT.

Pet-проект: разработка масштабируемого MVP для проверки архитектурных решений, асинхронного бэкенда и настройки CI/CD процессов.


## Возможности

- Регистрация и вход, пароли хранятся как bcrypt-хэши
- JWT-авторизация (Bearer token)
- CRUD товаров: пользователь управляет только своими
- Витрина с товарами других пользователей, постраничная (`limit`/`offset`)
- Заказы: нельзя купить свой товар и один товар дважды
- Личные заметки (CRUD)
- Внешние ключи с каскадным удалением: при удалении аккаунта удаляются его товары, заказы и заметки
- Миграции схемы БД через Alembic
- Валидация входных данных через Pydantic, Swagger UI из коробки
- 20 тестов на pytest, БД в памяти, реальные данные не затрагиваются
- CI на GitHub Actions: тесты, применение миграций на чистой БД, проверка синхронизации моделей и миграций
- Запуск одной командой через Docker Compose (приложение + PostgreSQL)

## Стек

| Область | Технологии |
|---|---|
| Язык / фреймворк | Python 3.12, FastAPI |
| БД и ORM | SQLAlchemy 2.0, Alembic, PostgreSQL (Docker) / SQLite (локально) |
| Авторизация | PyJWT, bcrypt |
| Инфраструктура | Docker, Docker Compose, GitHub Actions |
| Тесты | pytest, httpx |

## Быстрый старт

### Docker

```bash
git clone https://github.com/balobol229-cmd/mini-marketplace.git
cd mini-marketplace
docker compose up --build
```

API: http://localhost:8000, документация: http://localhost:8000/docs

Миграции применяются автоматически при старте контейнера. `SECRET_KEY` по умолчанию `devsecret`, для своего ключа: `SECRET_KEY=... docker compose up --build`.

Если запускали более старую версию проекта, сбросьте старую БД: `docker compose down -v`.

### Локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export SECRET_KEY=your_secret_key
alembic upgrade head
uvicorn main:app --reload
```

Без `DATABASE_URL` приложение использует SQLite-файл `users.db`.

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `SECRET_KEY` | Секрет для подписи JWT, обязательна | нет |
| `DATABASE_URL` | Строка подключения SQLAlchemy | `sqlite:///./users.db` |

Пример в файле `.env.example`.

## API

Все эндпоинты, кроме регистрации, логина и `/health`, требуют заголовок `Authorization: Bearer <token>`.

| Метод | Путь | Описание |
|---|---|---|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Вход, возвращает JWT |
| GET | `/auth/me` | Текущий пользователь |
| DELETE | `/auth/me` | Удалить аккаунт (каскадно товары, заказы, заметки) |
| POST, GET | `/products` | Создать товар, список своих товаров |
| GET, PATCH, DELETE | `/products/{id}` | Свой товар |
| GET | `/shop?limit=20&offset=0` | Витрина: товары других пользователей, постранично (limit 1–100) |
| POST | `/order?product_id=` | Купить товар |
| GET | `/order` | Мои заказы |
| GET, DELETE | `/order/{id}` | Мой заказ |
| POST, GET | `/notes` | Заметки |
| GET, PATCH, DELETE | `/notes/{id}` | Своя заметка |
| GET | `/health` | Проверка работоспособности |

### Пример

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
# {"access_token": "...", "token_type": "bearer"}

curl http://localhost:8000/auth/me -H "Authorization: Bearer <access_token>"
```

## Миграции

```bash
alembic upgrade head                              # применить
alembic revision --autogenerate -m "описание"      # создать после изменения models.py
alembic downgrade -1                              # откатить последнюю
```

## Тесты

```bash
pip install -r requirements-dev.txt
SECRET_KEY=test pytest -v
```

## Структура

```
main.py          точка входа, подключение роутеров, /health
database.py      движок и сессия SQLAlchemy
models.py        ORM-модели (внешние ключи, ограничения)
schemas.py       Pydantic-схемы
security.py      JWT и зависимость get_current_user
routers/         auth, products, shop, order, notes
alembic/         миграции схемы БД
tests/           pytest, БД в памяти
.github/         CI (GitHub Actions)
Dockerfile, compose.yaml, render.yaml
```

## Деплой на Render

В репозитории есть `render.yaml` (Blueprint): веб-сервис из Dockerfile и база PostgreSQL. В Render: New → Blueprint → выбрать этот репозиторий → Apply. `SECRET_KEY` создаётся автоматически, `DATABASE_URL` подставляется из базы, миграции применяются при старте.

## Что можно улучшить

- Refresh-токены и возможность отзыва токена
- Остатки товара и оплата
- Поиск и фильтры на витрине
- Rate limiting на логин
