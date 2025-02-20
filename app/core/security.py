from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)
security = HTTPBearer()
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera hash de la contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decodifica un token JWT"""
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    token = credentials.credentials
    decoded_token = decode_token(token)
    if decoded_token is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user_id = decoded_token.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token no contiene el user_id")
    return {"user_id": user_id}