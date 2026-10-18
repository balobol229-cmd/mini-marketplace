
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.orm import Session

from database import get_db
from models import UserDB



SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("нет SECRET_KEY")


security = HTTPBearer()    





def create_access_token(user_id:int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes = 60)

    }
    return jwt.encode(payload, SECRET_KEY, algorithm ="HS256")





def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
        ):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ["HS256"])
    except:
        raise HTTPException(status_code = 401, detail = "билет потух")
    

    user_id = int(payload["sub"])
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if user is None:
        raise HTTPException(status_code = 401, detail = "такого юзера в списке нет")
    return user
