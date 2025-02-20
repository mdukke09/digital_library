from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud.user import user as user_crud
from app.core.security import verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(
    login_data: LoginData,
    db: Session = Depends(get_db)
):
    user = user_crud.get_by_email(db, email=login_data.email)    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }