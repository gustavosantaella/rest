"""
Servicio de permisos usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from .permissions_repository import PermissionsRepository


@Injectable
class PermissionsService:
    """Servicio para lógica de negocio de permisos"""
    
    def __init__(self):
        pass
    
    def get_all_permissions(self, db: Session):
        """Obtener todos los permisos"""
        repo = PermissionsRepository(db)
        return repo.find_all()
    
    def get_permissions_by_module(self, db: Session):
        """Obtener permisos agrupados por módulo"""
        repo = PermissionsRepository(db)
        return repo.find_by_module()

