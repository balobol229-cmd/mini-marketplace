import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from models import UserDB
from schemas import UserPublic, UserRegister
from security import create_access_token, get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register")
def create_account(user_data: UserRegister, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.email == user_data.email).first():
        raise HTTPException(status_code=400, detail = "Пользователь уже загестрирован")
    new_account = UserDB(email = user_data.email, password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {"message": "Вы успешно зарегестрировались"}



@router.get("/me")
def show_my_account(current_user: UserDB = Depends(get_current_user)):
    return UserPublic(id = current_user.id, email = current_user.email)



@router.post("/login")
def confirm_registered(user_data: UserRegister, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if user and bcrypt.checkpw(user_data.password.encode('utf-8'), user.password.encode('utf-8')):
        
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code=401, detail = "Неверный логин или пароль")

