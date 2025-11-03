from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.configuration import BusinessConfiguration
from ..schemas.user import UserResponse, UserUpdate, UserCreate
from ..utils.dependencies import get_current_user, get_current_active_admin
from ..utils.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


def _build_user_response(user: User, db: Session) -> UserResponse:
    """Construye respuesta del usuario con el nombre del negocio"""
    business_name = None
    if user.business_id:
        business = (
            db.query(BusinessConfiguration)
            .filter(BusinessConfiguration.id == user.business_id)
            .first()
        )
        if business:
            business_name = business.business_name

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        dni=user.dni,
        country=user.country,
        business_id=user.business_id,
        is_active=user.is_active,
        created_at=user.created_at,
        business_name=business_name,
    )


@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return _build_user_response(current_user, db)


@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    # Filtrar usuarios del mismo negocio
    users = (
        db.query(User)
        .filter(User.business_id == current_user.business_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [_build_user_response(u, db) for u in users]


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """Crear un nuevo usuario en el negocio del administrador actual"""

    # Verificar si el email ya existe en este negocio
    existing = (
        db.query(User)
        .filter(
            User.email == user_data.email, User.business_id == current_user.business_id
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado en tu negocio",
        )

    # Verificar si el username ya existe en este negocio
    existing = (
        db.query(User)
        .filter(
            User.username == user_data.username,
            User.business_id == current_user.business_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado en tu negocio",
        )

    # Crear usuario
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        business_id=current_user.business_id,  # Mismo negocio del admin
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role,
        dni=user_data.dni,
        country=user_data.country,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return _build_user_response(new_user, db)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.business_id
            == current_user.business_id,  # Solo usuarios del mismo negocio
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return _build_user_response(user, db)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.business_id
            == current_user.business_id,  # Solo usuarios del mismo negocio
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # No permitir cambiar business_id
    if "business_id" in update_data:
        del update_data["business_id"]

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return _build_user_response(user, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.business_id
            == current_user.business_id,  # Solo usuarios del mismo negocio
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # No permitir eliminar el último administrador
    admin_count = (
        db.query(User)
        .filter(
            User.business_id == current_user.business_id,
            User.role == "admin",
            User.is_active == True,
        )
        .count()
    )

    if user.role == "admin" and admin_count <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar el último administrador del negocio",
        )

    db.delete(user)
    db.commit()
    return None
