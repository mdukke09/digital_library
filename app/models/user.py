from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    """Modelo de Usuario"""
    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    registration_date = Column(DateTime, nullable=False)
    
    # Relaciones
    borrowed_books = relationship("Book", back_populates="borrowed_by")