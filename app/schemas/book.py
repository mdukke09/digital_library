from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.author import Author
from app.schemas.user import User

class BookBase(BaseModel):
    """Esquema base de libro"""
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., description="Título del libro")
    publication_year: Optional[int] = Field(None, description="Año de publicación")
    author_id: int = Field(..., description="ID del autor")

class BookInDBBase(BookBase):
    """Esquema base para libro en DB"""
    id: int
    borrowed_by_id: Optional[int] = Field(None, description="ID del usuario que tiene prestado el libro")

class BookCreate(BookBase):
    """Esquema para crear libro"""
    pass

class BookUpdate(BaseModel):
    """Esquema para actualizar libro"""
    title: Optional[str] = Field(None, description="Título del libro")
    publication_year: Optional[int] = Field(None, description="Año de publicación")
    author_id: Optional[int] = Field(None, description="ID del autor")

class Book(BookInDBBase):
    """Esquema para respuesta de libro"""
    model_config = ConfigDict(from_attributes=True)
    author: Optional[Author] = None
    borrowed_by: Optional[User] = None