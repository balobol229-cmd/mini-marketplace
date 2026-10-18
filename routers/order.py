from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from models import OrderDB, ProductforsaleDB
from schemas import Orderpublic
from security import get_current_user


router = APIRouter(prefix="/order", tags=["order"])


@router.post("")
def open_order(product_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(ProductforsaleDB).filter(ProductforsaleDB.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code = 404, detail = "нет такой штуки здесь")
    if product.user_id == current_user.id:
        raise HTTPException(status_code = 400, detail = "нельзя купить товар, который вы уже купили")
    


    already = db.query(OrderDB).filter(OrderDB.product_id == product.id, OrderDB.user_id == current_user.id).first()
    if already:
        raise HTTPException(status_code = 400, detail = "нельяз купить один товар два раза")
  
    
    new_purchase = OrderDB(product_id=product_id, user_id = current_user.id)

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    return {"id": new_purchase.id, "user_id": new_purchase.user_id, "product_id":new_purchase.product_id }


@router.get("")
def show_my_purchases_orders(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    purchases_list = []

    purchases = db.query(OrderDB).filter(OrderDB.user_id == current_user.id).all()

    for my_purchases in purchases:
        purchases_public = Orderpublic(id = my_purchases.id, user_id = my_purchases.user_id, product_id = my_purchases.product_id)

        purchases_list.append(purchases_public)
    return purchases_list


@router.get("/{order_id}")
def show_exactly_purchases(order_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(OrderDB).filter(OrderDB.id == order_id).first()

    if not orders:
        raise HTTPException(status_code = 404, detail = "такой строки нет")

    if orders.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Такого ордера нет в списке")

    return {"id": orders.id, "product_id": orders.product_id, "user_id": orders.user_id}



@router.delete("/{order_id}")
def delete_order(order_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    order_for_delete = db.query(OrderDB).filter(OrderDB.id == order_id).first()

    if not order_for_delete:
        raise HTTPException(status_code = 404, detail = "Такого ордера нет")
    if order_for_delete.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Такой оффер не принадлежит тебе")
    db.delete(order_for_delete)
    db.commit()

    return {"ok": True}

