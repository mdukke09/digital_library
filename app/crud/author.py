from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate
from .base import CRUDBase

class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    """Operaciones CRUD específicas para autores"""
    pass

author = CRUDAuthor(Author)