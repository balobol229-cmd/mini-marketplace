# Mini Marketplace API

Backend мини-маркетплейса на FastAPI: регистрация, JWT-логин, товары и заказы.

## Стек
Python, FastAPI, SQLAlchemy, JWT, bcrypt, Docker, pytest

## Запуск
```bash
export SECRET_KEY=your_secret_key
pip install -r requirements.txt
uvicorn main:app --reload
```

Или через Docker:
```bash
docker compose -f Docker.compose.yaml up --build
```

Документация API после запуска: `http://127.0.0.1:8000/docs`

## Основные эндпоинты
- `POST /auth/register` — регистрация
- `POST /auth/login` — логин, выдаёт JWT
- `GET /auth/me` — текущий пользователь (Bearer)
- `POST /products` — создать товар
- `GET /products` — мои товары
- `POST /order` — купить товар
- `GET /orders` — мои заказы
- `GET /shop` — витрина

## Тесты
```bash
export SECRET_KEY=testsecret
pytest -v
```
