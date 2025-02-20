from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

def parse_date(value: str) -> datetime:
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid date format. Use DD/MM/YYYY or ISO format")
    return value

DateField = Annotated[datetime, BeforeValidator(parse_date)]

class AuthorBase(BaseModel):
    """Esquema base de autor"""
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., description="Nombre del autor")
    birth_date: Optional[DateField] = Field(None, description="Fecha de nacimiento del autor")

class AuthorCreate(AuthorBase):
    """Esquema para crear autor"""
    pass

class AuthorUpdate(BaseModel):
    """Esquema para actualizar autor"""
    name: Optional[str] = Field(None, description="Nombre del autor")
    birth_date: Optional[DateField] = Field(None, description="Fecha de nacimiento del autor")

class AuthorInDBBase(AuthorBase):
    """Esquema base para autor en DB"""
    id: int
    model_config = ConfigDict(from_attributes=True)

class Author(AuthorInDBBase):
    """Esquema para respuesta de autor"""
    books: List = []