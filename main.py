from fastapi import FastAPI

from routers import auth, notes, order, products, shop


# Схема БД создаётся миграциями: alembic upgrade head
app = FastAPI(title="Mini Marketplace API")

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(order.router)
app.include_router(products.router)
app.include_router(shop.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
