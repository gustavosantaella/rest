from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.permission import UserPermission
from ..schemas.permission import PermissionResponse, PermissionUpdate
from ..utils.dependencies import get_current_active_admin

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("/{user_id}", response_model=PermissionResponse)
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Obtener permisos de un usuario"""
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
    
    # Si no tiene permisos creados, crear unos por defecto
    if not user.permissions:
        permissions = UserPermission(
            user_id=user_id,
            can_access_dashboard=True,
            can_access_inventory=False,
            can_access_products=False,
            can_access_menu=False,
            can_access_tables=False,
            can_access_orders=False,
            can_access_users=False,
            can_access_configuration=False,
            can_access_reports=False
        )
        db.add(permissions)
        db.commit()
        db.refresh(permissions)
        return permissions
    
    return user.permissions


@router.put("/{user_id}", response_model=PermissionResponse)
def update_user_permissions(
    user_id: int,
    permission_update: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Actualizar permisos de un usuario"""
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
    
    # Si no tiene permisos, crearlos
    if not user.permissions:
        permissions = UserPermission(user_id=user_id)
        db.add(permissions)
        db.flush()
    else:
        permissions = user.permissions
    
    # Actualizar permisos
    update_data = permission_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(permissions, field, value)
    
    db.commit()
    db.refresh(permissions)
    return permissions

