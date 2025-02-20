from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")

class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str = Field(..., description="Contraseña del usuario")

class UserUpdate(BaseModel):
    """Esquema para actualizar usuario"""
    name: Optional[str] = Field(None, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico del usuario")
    password: Optional[str] = Field(None, description="Contraseña del usuario")

class UserInDBBase(UserBase):
    """Esquema base para usuario en DB"""
    id: int
    registration_date: datetime
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    """Esquema para respuesta de usuario"""
    borrowed_books: List = []