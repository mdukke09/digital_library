from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Book(BaseModel):
    """Modelo de Libro"""
    __tablename__ = "books"

    title = Column(String, nullable=False, index=True)
    publication_year = Column(Integer, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    borrowed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relaciones
    author = relationship("Author", back_populates="books")
    borrowed_by = relationship("User", back_populates="borrowed_books")