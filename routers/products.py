from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ProductDB, UserDB
from schemas import CreateProduct, ProductPublic
from security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


def _validate(product_data: CreateProduct) -> None:
    if not product_data.title.strip():
        raise HTTPException(status_code=400, detail="Название не должно быть пустым")
    if product_data.price <= 0:
        raise HTTPException(status_code=400, detail="Цена должна быть больше нуля")


def _get_own_product(product_id: int, user: UserDB, db: Session) -> ProductDB:
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if product.user_id != user.id:
        raise HTTPException(status_code=403, detail="Это не ваш товар")
    return product


@router.post("", response_model=ProductPublic)
def create_product(
    product_data: CreateProduct,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _validate(product_data)

    product = ProductDB(
        title=product_data.title, price=product_data.price, user_id=current_user.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=list[ProductPublic])
def list_my_products(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(ProductDB).filter(ProductDB.user_id == current_user.id).all()


@router.get("/{product_id}", response_model=ProductPublic)
def get_my_product(
    product_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_own_product(product_id, current_user, db)


@router.patch("/{product_id}", response_model=ProductPublic)
def update_product(
    product_id: int,
    product_data: CreateProduct,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _validate(product_data)

    product = _get_own_product(product_id, current_user, db)
    product.title = product_data.title
    product.price = product_data.price
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = _get_own_product(product_id, current_user, db)
    db.delete(product)
    db.commit()
    return {"ok": True}
