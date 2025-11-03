from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.configuration import BusinessConfiguration
from ..schemas.user import UserResponse
from ..schemas.profile import ProfileUpdate, PasswordChange
from ..utils.dependencies import get_current_user, get_current_active_admin, get_user_permissions
from ..utils.security import verify_password, get_password_hash

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Obtener perfil del usuario actual"""
    return current_user


@router.get("/my-permissions")
def get_my_permissions(current_user: User = Depends(get_current_user)):
    """Debug: Ver todos los permisos del usuario actual"""
    permissions = list(get_user_permissions(current_user))
    
    return {
        "user": current_user.username,
        "role": current_user.role,
        "custom_roles": [{"id": r.id, "name": r.name} for r in current_user.custom_roles] if current_user.custom_roles else [],
        "permissions": permissions,
        "total_permissions": len(permissions)
    }


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Actualizar perfil del usuario actual"""
    update_data = profile_update.model_dump(exclude_unset=True)
    
    # Verificar si el email ya está en uso por otro usuario
    if "email" in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso por otro usuario",
            )
    
    # Verificar si el DNI ya está en uso por otro usuario
    if "dni" in update_data and update_data["dni"]:
        existing_user = db.query(User).filter(
            User.dni == update_data["dni"],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El DNI ya está en uso por otro usuario",
            )
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cambiar contraseña del usuario actual"""
    
    # Verificar contraseña actual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta",
        )
    
    # Actualizar contraseña
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}


@router.delete("/delete-account-permanently", status_code=status.HTTP_200_OK)
def delete_account_permanently(
    password_confirmation: str,
    current_user: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db),
):
    """
    Eliminar permanentemente la cuenta del usuario y TODOS los datos del negocio.
    
    ADVERTENCIA: Esta acción es IRREVERSIBLE y eliminará:
    - Todos los usuarios del negocio
    - Todos los productos y categorías
    - Todas las órdenes e items
    - Todos los métodos de pago
    - Todo el menú y sus categorías
    - Todas las mesas
    - Toda la configuración del negocio
    - Todos los socios
    
    Solo los administradores pueden realizar esta acción.
    """
    
    # Verificar que el usuario es administrador
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar permanentemente el negocio",
        )
    
    # Verificar contraseña para confirmar acción crítica
    if not verify_password(password_confirmation, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta. No se puede proceder con la eliminación",
        )
    
    # Verificar que el usuario pertenece a un negocio
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No estás asociado a ningún negocio",
        )
    
    # Obtener el negocio
    business = db.query(BusinessConfiguration).filter(
        BusinessConfiguration.id == current_user.business_id
    ).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Negocio no encontrado",
        )
    
    business_name = business.business_name
    
    try:
        # Eliminar el negocio completo
        # Gracias al CASCADE configurado en las foreign keys, esto eliminará:
        # - Todos los usuarios asociados
        # - Todos los partners
        # - Y cualquier otra relación con CASCADE
        
        db.delete(business)
        db.commit()
        
        return {
            "message": f"El negocio '{business_name}' y todos sus datos han sido eliminados permanentemente",
            "warning": "Esta acción es irreversible. Todos los datos han sido eliminados de la base de datos"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el negocio: {str(e)}",
        )

