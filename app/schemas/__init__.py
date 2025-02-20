from .user import User, UserCreate, UserUpdate, UserInDBBase
from .author import Author, AuthorCreate, AuthorUpdate, AuthorInDBBase
from .book import Book, BookCreate, BookUpdate, BookInDBBase

# Resolvemos las referencias circulares
Book.model_rebuild()
Author.model_rebuild()
User.model_rebuild()