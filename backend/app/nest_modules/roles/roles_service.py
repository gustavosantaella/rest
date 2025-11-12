"""
Servicio de roles usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from .roles_repository import RolesRepository
from ...models.role_permission import Role


@Injectable
class RolesService:
    """Servicio para lógica de negocio de roles"""
    
    def __init__(self):
        pass
    
    def get_roles(self, business_id: int, skip: int, limit: int, db: Session) -> List[Role]:
        """Obtener lista de roles del negocio"""
        repo = RolesRepository(db)
        return repo.find_all(business_id, skip, limit)
    
    def get_role_by_id(self, role_id: int, business_id: int, db: Session) -> Role:
        """Obtener rol por ID"""
        repo = RolesRepository(db)
        role = repo.find_by_id(role_id, business_id)
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        return role
    
    def get_user_roles(self, user_id: int, business_id: int, db: Session):
        """Obtener roles de un usuario"""
        repo = RolesRepository(db)
        roles = repo.find_by_user_id(user_id, business_id)
        
        return [{"id": r.id, "name": r.name, "description": r.description} for r in roles]
    
    def create_role(self, name: str, description: str, business_id: int, db: Session) -> Role:
        """Crear nuevo rol"""
        repo = RolesRepository(db)
        
        # Validar que no exista un rol con el mismo nombre
        existing = repo.find_by_name(name, business_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un rol con ese nombre en tu negocio"
            )
        
        return repo.create({
            'name': name,
            'description': description,
            'business_id': business_id
        })
    
    def delete_role(self, role_id: int, business_id: int, db: Session):
        """Eliminar rol"""
        repo = RolesRepository(db)
        role = repo.find_by_id(role_id, business_id)
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        repo.soft_delete(role)

