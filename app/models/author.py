from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class Author(BaseModel):
    """Modelo de Autor"""
    __tablename__ = "authors"

    name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=True)
    
    # Relaciones
    books = relationship("Book", back_populates="author")