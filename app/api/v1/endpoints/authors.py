from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.dependencies import get_db
from app.core.security import get_current_user
from app.crud.author import author
from app.schemas.author import Author, AuthorCreate, AuthorUpdate

router = APIRouter()

@router.post("/", response_model=Author, summary="Crear autor")
def create_author(
    *,
    db: Session = Depends(get_db),
    author_in: AuthorCreate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Crea un nuevo autor en el sistema.
    """    
    # Validar que la fecha de nacimiento no sea futura
    if author_in.birth_date and author_in.birth_date > datetime.now():
        raise HTTPException(
            status_code=400,
            detail="La fecha de nacimiento no puede ser futura"
        )
    return author.create(db, obj_in=author_in)

@router.get("/", response_model=List[Author], summary="Listar autores")
def read_authors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Recupera todos los autores.
    """
    authors = author.get_multi(db, skip=skip, limit=limit)
    return authors

@router.get("/{author_id}", response_model=Author, summary="Obtener autor")
def read_author(
    *,
    db: Session = Depends(get_db),
    author_id: int
) -> Any:
    """
    Obtiene un autor específico por su ID.
    """
    db_author = author.get(db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return db_author

@router.put("/{author_id}", response_model=Author, summary="Actualizar autor")
def update_author(
    *,
    db: Session = Depends(get_db),
    author_id: int,
    author_in: AuthorUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Actualiza un autor existente.
    """
    db_author = author.get(db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    # Validar fecha de nacimiento si se proporciona
    if author_in.birth_date and author_in.birth_date > datetime.now():
        raise HTTPException(
            status_code=400,
            detail="La fecha de nacimiento no puede ser futura"
        )
    return author.update(db, db_obj=db_author, obj_in=author_in)

@router.delete("/{author_id}", response_model=Author, summary="Eliminar autor")
def delete_author(
    *,
    db: Session = Depends(get_db),
    author_id: int,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Elimina un autor del sistema.
    """
    db_author = author.get(db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    # Verificar si el autor tiene libros asociados
    if db_author.books:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el autor porque tiene libros asociados"
        )
    
    return author.remove(db, id=author_id)