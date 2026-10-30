import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import UserDB
from schemas import UserPublic, UserRegister
from security import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")

    hashed = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt())
    db.add(UserDB(email=user_data.email, hashed_password=hashed.decode("utf-8")))
    db.commit()

    return {"message": "Вы успешно зарегистрировались"}


@router.post("/login")
def login(user_data: UserRegister, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    password_ok = user and bcrypt.checkpw(
        user_data.password.encode("utf-8"), user.hashed_password.encode("utf-8")
    )
    if not password_ok:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return {"access_token": create_access_token(user.id), "token_type": "bearer"}


@router.get("/me", response_model=UserPublic)
def me(current_user: UserDB = Depends(get_current_user)):
    return current_user


@router.delete("/me")
def delete_me(
    current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Удаляет аккаунт; товары, заказы и заметки удаляются каскадом на уровне БД."""
    db.delete(current_user)
    db.commit()
    return {"ok": True}
