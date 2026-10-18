from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db

from models import ProductforsaleDB
from schemas import ProductPublic
from security import get_current_user

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get("")
def show_shop(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    shop_list = []

    open_shop_other_users = db.query(ProductforsaleDB).filter(ProductforsaleDB.user_id != current_user.id).all()

    for shop in open_shop_other_users:
        shopforsalespublic = ProductPublic(id = shop.id, title = shop.title, price = shop.price) 

    
    
        shop_list.append(shopforsalespublic)
    return shop_list

