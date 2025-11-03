from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models.user import User, UserRole
from ..models.role_permission import Role, Permission
from ..utils.security import decode_access_token
from typing import List, Set

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = decode_access_token(token)
    if username is None:
        raise credentials_exception

    # Buscar usuario con roles personalizados cargados (solo usuarios no eliminados)
    user = (
        db.query(User)
        .options(joinedload(User.custom_roles).joinedload(Role.permissions))
        .filter(
            User.username == username,
            User.deleted_at.is_(None),  # Solo usuarios no eliminados
        )
        .first()
    )
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )

    return user


def get_user_permissions(user: User) -> Set[str]:
    """Obtiene todos los permisos de un usuario desde sus roles personalizados"""
    permissions = set()
    if user.custom_roles:
        for role in user.custom_roles:
            if role.permissions:
                for permission in role.permissions:
                    permissions.add(permission.code)
    return permissions


def has_permission(user: User, permission_code: str) -> bool:
    """Verifica si un usuario tiene un permiso específico"""
    # Administradores tienen todos los permisos
    if user.role == UserRole.ADMIN:
        return True

    user_permissions = get_user_permissions(user)
    return permission_code in user_permissions


def has_any_permission(user: User, permission_codes: List[str]) -> bool:
    """Verifica si un usuario tiene al menos uno de los permisos especificados"""
    # Administradores tienen todos los permisos
    if user.role == UserRole.ADMIN:
        return True

    user_permissions = get_user_permissions(user)
    return any(perm in user_permissions for perm in permission_codes)


async def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Solo administradores - Acceso total"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden acceder a este recurso",
        )
    return current_user


async def get_current_active_manager(
    current_user: User = Depends(get_current_user),
) -> User:
    """Administradores, Managers o usuarios con permisos relevantes"""
    # Admins y Managers siempre tienen acceso
    if current_user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        return current_user

    # Verificar permisos personalizados (inventory, products)
    if has_any_permission(
        current_user, ["inventory.manage", "products.create", "products.edit"]
    ):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos suficientes para gestionar inventario/productos",
    )


async def get_current_active_chef(
    current_user: User = Depends(get_current_user),
) -> User:
    """Cocineros pueden ver órdenes - Compatible con permisos personalizados"""
    # Admins, Managers y Chefs siempre tienen acceso
    if current_user.role in [UserRole.ADMIN, UserRole.MANAGER, UserRole.CHEF]:
        return current_user

    # Verificar permisos personalizados de órdenes
    if has_any_permission(
        current_user, ["orders.view", "orders.create", "orders.edit"]
    ):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos suficientes para ver órdenes",
    )


async def check_config_permission(
    current_user: User = Depends(get_current_user),
) -> User:
    """Verifica acceso a configuración"""
    # Administradores siempre tienen acceso
    if current_user.role == UserRole.ADMIN:
        return current_user

    # Verificar permisos personalizados de configuración
    if has_any_permission(current_user, ["config.view", "config.edit"]):
        return current_user

    return current_user
    # raise HTTPException(
    #     status_code=status.HTTP_403_FORBIDDEN,
    #     detail="No tienes permisos para acceder a la configuración",
    # )
