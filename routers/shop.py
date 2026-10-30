from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import ProductDB, UserDB
from schemas import ProductPublic
from security import get_current_user

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get("", response_model=list[ProductPublic])
def show_shop(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Витрина: товары всех пользователей, кроме собственных."""
    return db.query(ProductDB).filter(ProductDB.user_id != current_user.id).all()
