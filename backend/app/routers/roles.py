from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.role_permission import Role, Permission, role_permissions
from ..schemas.role_permission import (
    RoleCreate, RoleUpdate, RoleResponse,
    PermissionResponse, UserRolesUpdate, UserRolesResponse
)
from ..utils.dependencies import get_current_active_admin

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=List[RoleResponse])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Obtener todos los roles del negocio"""
    # Verificar que el usuario tenga un negocio asignado
    if not current_user.business_id:
        return []  # Retornar lista vacía si no tiene negocio
    
    roles = db.query(Role).filter(
        Role.business_id == current_user.business_id,
        Role.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Obtener un rol específico"""
    role = db.query(Role).filter(
        Role.id == role_id,
        Role.business_id == current_user.business_id,
        Role.deleted_at.is_(None)
    ).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    return role


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Crear un nuevo rol"""
    # Verificar que el usuario tenga un negocio asignado
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes completar el registro de tu negocio primero en Configuración"
        )
    
    # Verificar que el nombre no exista en el negocio
    existing = db.query(Role).filter(
        Role.name == role_data.name,
        Role.business_id == current_user.business_id,
        Role.deleted_at.is_(None)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con ese nombre"
        )
    
    # Crear rol
    new_role = Role(
        business_id=current_user.business_id,
        name=role_data.name,
        description=role_data.description,
        is_active=role_data.is_active
    )
    db.add(new_role)
    db.flush()
    
    # Asignar permisos
    if role_data.permission_ids:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids)
        ).all()
        new_role.permissions = permissions
    
    db.commit()
    db.refresh(new_role)
    return new_role


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Actualizar un rol"""
    role = db.query(Role).filter(
        Role.id == role_id,
        Role.business_id == current_user.business_id,
        Role.deleted_at.is_(None)
    ).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Actualizar datos básicos
    update_data = role_data.model_dump(exclude_unset=True, exclude={'permission_ids'})
    for field, value in update_data.items():
        setattr(role, field, value)
    
    # Actualizar permisos si se proporcionan
    if role_data.permission_ids is not None:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids)
        ).all()
        role.permissions = permissions
    
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Eliminar un rol (soft delete)"""
    from datetime import datetime
    
    role = db.query(Role).filter(
        Role.id == role_id,
        Role.business_id == current_user.business_id,
        Role.deleted_at.is_(None)
    ).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    
    # Soft delete
    role.deleted_at = datetime.now()
    db.commit()
    return None


# User Roles Assignment
@router.get("/user/{user_id}/roles", response_model=UserRolesResponse)
def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Obtener roles asignados a un usuario"""
    user = db.query(User).filter(
        User.id == user_id,
        User.business_id == current_user.business_id,
        User.deleted_at.is_(None)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserRolesResponse(
        user_id=user.id,
        roles=user.custom_roles
    )


@router.put("/user/{user_id}/roles", response_model=UserRolesResponse)
def update_user_roles(
    user_id: int,
    roles_data: UserRolesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Asignar roles a un usuario"""
    user = db.query(User).filter(
        User.id == user_id,
        User.business_id == current_user.business_id,
        User.deleted_at.is_(None)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Obtener roles del mismo negocio
    roles = db.query(Role).filter(
        Role.id.in_(roles_data.role_ids),
        Role.business_id == current_user.business_id,
        Role.deleted_at.is_(None)
    ).all()
    
    # Asignar roles al usuario
    user.custom_roles = roles
    
    db.commit()
    db.refresh(user)
    
    return UserRolesResponse(
        user_id=user.id,
        roles=user.custom_roles
    )

