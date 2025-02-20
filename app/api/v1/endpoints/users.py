from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.security import get_current_user
from app.crud.user import user as user_crud
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.email_service import send_welcome_email
from app.utils.validation import is_password_valid

router = APIRouter()

@router.post("/", response_model=User, summary="Crear usuario")
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Crea un nuevo usuario en el sistema.

    - **name**: Nombre del usuario
    - **email**: Correo electrónico del usuario
    - **password**: Contraseña del usuario
    """
    # Validar que el email no esté registrado
    user_exists = user_crud.get_by_email(db, email=user_in.email)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con este email"
        )
    
    # Validar complejidad de la contraseña
    if not is_password_valid(user_in.password):
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números"
        )
    
    user_exists = user_crud.get_by_email(db, email=user_in.email)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con este email."
        )
    new_user = user_crud.create(db, obj_in=user_in)
    send_welcome_email(new_user.email)

    return new_user

@router.get("/", response_model=List[User], summary="Listar usuarios")
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
) -> Any:
    """
    Recupera una lista de usuarios.

    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a retornar
    """
    users = user_crud.get_multi(db, skip=skip, limit=limit)

    return users

@router.get("/{user_id}", response_model=User, summary="Obtener usuario")
def read_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Obtiene un usuario específico por su ID.

    - **user_id**: ID del usuario a recuperar
    """
    db_user = user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return db_user

@router.put("/{user_id}", response_model=User, summary="Actualizar usuario")
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Actualiza un usuario existente.

    - **name**: Nuevo nombre del usuario (opcional)
    - **email**: Nuevo correo electrónico del usuario (opcional)
    - **password**: Nueva contraseña del usuario (opcional)
    """
    # Verificar que el usuario existe
    db_user = user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Validar email único si se está actualizando
    if user_in.email and user_in.email != db_user.email:
        existing_user = user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con este email"
            )
    
    # Validar contraseña si se está actualizando
    if user_in.password and not is_password_valid(user_in.password):
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números"
        )
    
    return user_crud.update(db, db_obj=db_user, obj_in=user_in)

@router.delete("/{user_id}", response_model=User, summary="Eliminar usuario")
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Elimina un usuario del sistema.

    - **user_id**: ID del usuario a eliminar
    """
    # Verificar que el usuario existe
    db_user = user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar si el usuario tiene libros prestados
    if db_user.borrowed_books:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el usuario porque tiene libros prestados"
        )
    
    return user_crud.remove(db, id=user_id)