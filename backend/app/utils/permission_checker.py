"""
Sistema de validación de permisos personalizados
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserRole
from ..models.role_permission import Permission
from ..utils.dependencies import get_current_user
from typing import List


async def check_permission(
    permission_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Verifica si el usuario tiene un permiso específico
    Los administradores siempre tienen acceso
    """
    # Administradores tienen acceso total
    if current_user.role == UserRole.ADMIN:
        return current_user
    
    # Verificar si el usuario tiene el permiso en alguno de sus roles personalizados
    user_permissions = set()
    
    if current_user.custom_roles:
        for role in current_user.custom_roles:
            for permission in role.permissions:
                user_permissions.add(permission.code)
    
    if permission_code in user_permissions:
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"No tienes permiso para realizar esta acción. Se requiere: {permission_code}"
    )


def require_permission(permission_code: str):
    """
    Decorator para endpoints que requieren un permiso específico
    Uso: current_user: User = Depends(require_permission("products.create"))
    """
    async def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        return await check_permission(permission_code, current_user, db)
    
    return permission_dependency


def require_any_permission(permission_codes: List[str]):
    """
    Verifica si el usuario tiene AL MENOS UNO de los permisos especificados
    Útil para endpoints que pueden ser accedidos por diferentes roles
    """
    async def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        # Administradores tienen acceso total
        if current_user.role == UserRole.ADMIN:
            return current_user
        
        # Recopilar todos los permisos del usuario
        user_permissions = set()
        if current_user.custom_roles:
            for role in current_user.custom_roles:
                for permission in role.permissions:
                    user_permissions.add(permission.code)
        
        # Verificar si tiene al menos uno de los permisos requeridos
        for perm_code in permission_codes:
            if perm_code in user_permissions:
                return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tienes permiso para realizar esta acción. Se requiere uno de: {', '.join(permission_codes)}"
        )
    
    return permission_dependency

