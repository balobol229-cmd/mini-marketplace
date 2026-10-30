from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import OrderDB, ProductDB, UserDB
from schemas import OrderPublic
from security import get_current_user

router = APIRouter(prefix="/order", tags=["order"])


def _get_own_order(order_id: int, user: UserDB, db: Session) -> OrderDB:
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Это не ваш заказ")
    return order


@router.post("", response_model=OrderPublic)
def create_order(
    product_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if product.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Нельзя купить собственный товар")

    already_bought = (
        db.query(OrderDB)
        .filter(OrderDB.product_id == product.id, OrderDB.user_id == current_user.id)
        .first()
    )
    if already_bought:
        raise HTTPException(status_code=400, detail="Этот товар уже куплен")

    order = OrderDB(product_id=product.id, user_id=current_user.id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderPublic])
def list_my_orders(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(OrderDB).filter(OrderDB.user_id == current_user.id).all()


@router.get("/{order_id}", response_model=OrderPublic)
def get_my_order(
    order_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_own_order(order_id, current_user, db)


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = _get_own_order(order_id, current_user, db)
    db.delete(order)
    db.commit()
    return {"ok": True}
