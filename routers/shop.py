from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import ProductDB, UserDB
from schemas import ProductPublic
from security import get_current_user

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get("", response_model=list[ProductPublic])
def show_shop(
    limit: int = Query(20, ge=1, le=100, description="Сколько товаров вернуть"),
    offset: int = Query(0, ge=0, description="Сколько товаров пропустить"),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Витрина: товары других пользователей, постранично."""
    return (
        db.query(ProductDB)
        .filter(ProductDB.user_id != current_user.id)
        .order_by(ProductDB.id)
        .limit(limit)
        .offset(offset)
        .all()
    )
