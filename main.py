from fastapi import FastAPI



from database import engine
from models import  Base
from routers import auth, notes, order, products, shop 


Base.metadata.create_all(bind=engine)


app = FastAPI()





app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(order.router)
app.include_router(products.router)
app.include_router(shop.router)