"""
Servicio de perfil de usuario usando PyNest
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ...models.user import User
from ...schemas.profile import ProfileUpdate, PasswordChange
from ...utils.security import verify_password, get_password_hash
from ...utils.dependencies import get_user_permissions


@Injectable
class ProfileService:
    """Servicio para manejo del perfil de usuario"""
    
    def __init__(self):
        pass
    
    def get_my_profile(self, user: User):
        """Obtener perfil del usuario actual"""
        return user
    
    def get_my_permissions(self, user: User):
        """Obtener permisos del usuario actual"""
        permissions = list(get_user_permissions(user))
        
        return {
            "user": user.username,
            "role": user.role,
            "custom_roles": [{"id": r.id, "name": r.name} for r in user.custom_roles] if user.custom_roles else [],
            "permissions": permissions,
            "total_permissions": len(permissions)
        }
    
    def update_profile(self, user: User, profile_update: ProfileUpdate, db: Session):
        """Actualizar perfil del usuario"""
        update_data = profile_update.model_dump(exclude_unset=True)
        
        # Verificar email duplicado
        if "email" in update_data:
            existing = db.query(User).filter(
                User.email == update_data["email"],
                User.id != user.id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está en uso por otro usuario"
                )
        
        # Verificar DNI duplicado
        if "dni" in update_data and update_data["dni"]:
            existing = db.query(User).filter(
                User.dni == update_data["dni"],
                User.id != user.id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI ya está en uso por otro usuario"
                )
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def change_password(self, user: User, password_data: PasswordChange, db: Session):
        """Cambiar contraseña del usuario"""
        # Verificar contraseña actual
        if not verify_password(password_data.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña actual es incorrecta"
            )
        
        # Actualizar contraseña
        user.hashed_password = get_password_hash(password_data.new_password)
        db.commit()
        
        return {"message": "Contraseña actualizada exitosamente"}

