from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from models import ProductforsaleDB
from schemas import CreateProduct, ProductPublic
from security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.post("")
def create_product(product_data: CreateProduct, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not product_data.title.strip():
        raise HTTPException(status_code = 400, detail = "поле не должно быть пустым")


    if product_data.price <= 0:
        raise HTTPException(status_code = 400, detail = "цена не должна быть равна 0")

    productforsale = ProductforsaleDB(title = product_data.title, price = product_data.price, user_id = current_user.id) 
    
    db.add(productforsale)
    db.commit()
    db.refresh(productforsale)
    
    return {"id": productforsale.id, "title": productforsale.title, "price": productforsale.price, "user_id": productforsale.user_id}




@router.get("")
def ShowProduct(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    productforsale_list = []

    productforsales = db.query(ProductforsaleDB).filter(ProductforsaleDB.user_id == current_user.id).all()
    for productforsale in productforsales:
        productforsale_public = ProductPublic(price = productforsale.price, title = productforsale.title, id = productforsale.id)

        productforsale_list.append(productforsale_public)

    return productforsale_list


@router.delete("/{product_id}")
def DeleteProduct(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    productfordelete = db.query(ProductforsaleDB).filter(ProductforsaleDB.id == product_id).first()

    if not productfordelete:
        raise HTTPException(status_code = 404, detail = "Такого продукта нет в списке")
    if productfordelete.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Такого продукта нет в вашем профиле")

    db.delete(productfordelete)
    db.commit()
    return {"ok": True}


        
@router.patch("/{product_id}")
def UpdateProduct(product_data: CreateProduct, product_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not product_data.title.strip():
        raise HTTPException(status_code = 400, detail = "нельзя обновить на воздух")
    
    if product_data.price <= 0:
        raise HTTPException(status_code = 400, detail = "нельзя обновить на цену ниже или равную нулю")

    productforupdate = db.query(ProductforsaleDB).filter(ProductforsaleDB.id == product_id).first()


    if not productforupdate:
        raise HTTPException(status_code = 404, detail = "Такого продукта нет в списке")
    if productforupdate.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Такого продукта нет в вашем профиле")

    productforupdate.title = product_data.title
    productforupdate.price = product_data.price

    db.commit()
    return {"id": productforupdate.id, "title": productforupdate.title, "price": productforupdate.price}




@router.get("/{product_id}")
def getproudct(product_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    getallproduct = db.query(ProductforsaleDB).filter(ProductforsaleDB.id == product_id).first()
    if not getallproduct:
        raise HTTPException(status_code = 404, detail = "такого продукта нет")

    if getallproduct.user_id != current_user.id:
        raise HTTPException (status_code = 403, detail = "такой задачи нет в твоем профиле")

    
    return {"id": getallproduct.id, "title": getallproduct.title, "price": getallproduct.price}


