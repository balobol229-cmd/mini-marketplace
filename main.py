from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine
from models import Base
from routers import auth, notes, order, products, shop


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Mini Marketplace API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(order.router)
app.include_router(products.router)
app.include_router(shop.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
