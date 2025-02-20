from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from .base import CRUDBase

class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    """Operaciones CRUD específicas para libros"""
    def search_books(
        self, 
        db: Session, 
        *, 
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        publication_year: Optional[int] = None
    ) -> List[Book]:
        """Busca libros por título, autor o año de publicación"""
        query = db.query(self.model)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author_id:
            query = query.filter(Book.author_id == author_id)
        if publication_year:
            query = query.filter(Book.publication_year == publication_year)
        return query.all()

    def borrow_book(self, db: Session, *, book_id: int, user_id: int) -> Book:
        """Registra el préstamo de un libro"""
        book = self.get(db, id=book_id)
        if book and not book.borrowed_by_id:
            book.borrowed_by_id = user_id
            db.add(book)
            db.commit()
            db.refresh(book)
        return book

    def return_book(self, db: Session, *, book_id: int) -> Book:
        """Registra la devolución de un libro"""
        book = self.get(db, id=book_id)
        if book and book.borrowed_by_id:
            book.borrowed_by_id = None
            db.add(book)
            db.commit()
            db.refresh(book)
        return book
    
book = CRUDBook(Book)