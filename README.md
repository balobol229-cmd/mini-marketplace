# Mini Marketplace API

Backend мини-маркетплейса на FastAPI. Пользователи регистрируются, выставляют товары на продажу и покупают товары друг у друга. Авторизация через JWT.

Учебный проект: хотел разобраться, как устроен backend с авторизацией, базой данных, тестами и контейнеризацией.

## Возможности

- Регистрация и вход, пароли хранятся как bcrypt-хэши
- JWT-авторизация (Bearer token)
- CRUD товаров: пользователь управляет только своими
- Витрина с товарами других пользователей
- Заказы: нельзя купить свой товар и один товар дважды
- Личные заметки (CRUD)
- Валидация входных данных через Pydantic, Swagger UI из коробки
- 17 тестов на pytest, БД в памяти, реальные данные не затрагиваются
- Запуск одной командой через Docker Compose (приложение + PostgreSQL)

## Стек

| Область | Технологии |
|---|---|
| Язык / фреймворк | Python 3.12, FastAPI |
| БД и ORM | SQLAlchemy 2.0, PostgreSQL (Docker) / SQLite (локально) |
| Авторизация | PyJWT, bcrypt |
| Инфраструктура | Docker, Docker Compose |
| Тесты | pytest, httpx |

## Быстрый старт

### Docker

```bash
git clone https://github.com/balobol229-cmd/mini-marketplace.git
cd mini-marketplace
docker compose up --build
```

API: http://localhost:8000, документация: http://localhost:8000/docs

`SECRET_KEY` по умолчанию `devsecret`. Для своего ключа: `SECRET_KEY=... docker compose up --build`.

### Локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export SECRET_KEY=your_secret_key
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
| POST, GET | `/products` | Создать товар, список своих товаров |
| GET, PATCH, DELETE | `/products/{id}` | Свой товар |
| GET | `/shop` | Витрина: товары других пользователей |
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

## Тесты

```bash
pip install -r requirements-dev.txt
SECRET_KEY=test pytest -v
```

## Структура

```
main.py          точка входа, подключение роутеров, /health
database.py      движок и сессия SQLAlchemy
models.py        ORM-модели
schemas.py       Pydantic-схемы
security.py      JWT и зависимость get_current_user
routers/         auth, products, shop, order, notes
tests/           pytest, БД в памяти
Dockerfile, compose.yaml
```

## Что можно улучшить

- Миграции через Alembic вместо `create_all`
- Внешние ключи и каскадное удаление в моделях
- Refresh-токены и возможность отзыва токена
- Пагинация на витрине
- CI на GitHub Actions
