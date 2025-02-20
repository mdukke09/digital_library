from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.security import get_current_user
from app.crud.book import book
from app.schemas.book import Book, BookCreate, BookUpdate
from app.crud.author import author as author_crud
from app.crud.user import user as user_crud
from fastapi.encoders import jsonable_encoder
import json

router = APIRouter()

@router.post("/", response_model=Book, summary="Crear libro")
def create_book(
    *,
    db: Session = Depends(get_db),
    book_in: BookCreate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Crea un nuevo libro en el sistema.

    - **title**: Título del libro
    - **author_id**: ID del autor del libro
    - **publication_year**: Año de publicación (opcional)
    """
    # Validar que el autor existe
    db_author = author_crud.get(db, id=book_in.author_id)
    if not db_author:
        raise HTTPException(
            status_code=404,
            detail=f"El autor con ID {book_in.author_id} no existe"
        )
    print('Entro al create')
    
    created_book = book.create(db, obj_in=book_in)
    
    # Convertir el objeto SQLAlchemy a un diccionario
    book_dict = jsonable_encoder(created_book)
    
    # Convertir el diccionario a un objeto Pydantic (Book)
    return Book.model_validate(book_dict)

@router.get("/", response_model=List[Book], summary="Listar libros")
def read_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Recupera una lista de libros.

    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a retornar
    """
    books = book.get_multi(db, skip=skip, limit=limit)
    return books

@router.get("/{book_id}", response_model=Book, summary="Obtener libro")
def read_book(
    *,
    db: Session = Depends(get_db),
    book_id: int
) -> Any:
    """
    Obtiene un libro específico por su ID.

    - **book_id**: ID del libro a recuperar
    """
    db_book = book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return db_book

@router.put("/{book_id}", response_model=Book, summary="Actualizar libro")
def update_book(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    book_in: BookUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Actualiza un libro existente.
    """
    db_book = book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # Si se está actualizando el autor, validar que existe
    if book_in.author_id is not None:
        db_author = author_crud.get(db, id=book_in.author_id)
        if not db_author:
            raise HTTPException(
                status_code=404,
                detail=f"El autor con ID {book_in.author_id} no existe"
            )
    
    return book.update(db, db_obj=db_book, obj_in=book_in)

@router.delete("/{book_id}", response_model=Book, summary="Eliminar libro")
def delete_book(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Elimina un libro del sistema.

    - **book_id**: ID del libro a eliminar
    """
    db_book = book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book.remove(db, id=book_id)

@router.get("/search/", response_model=List[Book], summary="Buscar libros")
def search_books(
    *,
    db: Session = Depends(get_db),
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    publication_year: Optional[int] = None,
) -> Any:
    """
    Busca libros por título, autor o año de publicación.
    """
    # Validar que el autor existe si se proporciona
    if author_id is not None:
        db_author = author_crud.get(db, id=author_id)
        if not db_author:
            raise HTTPException(
                status_code=404,
                detail=f"El autor con ID {author_id} no existe"
            )
    
    books = book.search_books(
        db, 
        title=title, 
        author_id=author_id, 
        publication_year=publication_year
    )
    return books

@router.post("/{book_id}/borrow", response_model=Book, summary="Prestar libro")
def borrow_book(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Registra el préstamo de un libro a un usuario.
    """
    # Validar que el libro existe
    db_book = book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if db_book.borrowed_by_id:
        raise HTTPException(
            status_code=400, 
            detail=f"El libro ya está prestado al usuario con ID {db_book.borrowed_by_id}"
        )
    
    # Validar que el usuario existe (opcional, ya que current_user ya lo garantiza)
    user = user_crud.get(db, id=current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    return book.borrow_book(db, book_id=book_id, user_id=current_user["user_id"])

@router.post("/{book_id}/return", response_model=Book, summary="Devolver libro")
def return_book(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Registra la devolución de un libro.

    - **book_id**: ID del libro a devolver
    """
    db_book = book.get(db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not db_book.borrowed_by_id:
        raise HTTPException(status_code=400, detail="El libro no está prestado")
    if db_book.borrowed_by_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="No puedes devolver un libro que no te prestaron")
    return book.return_book(db, book_id=book_id)