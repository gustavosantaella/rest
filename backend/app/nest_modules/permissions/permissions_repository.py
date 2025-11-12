"""
Repositorio de permisos - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ...models.permission import UserPermission


class PermissionsRepository:
    """Repositorio para operaciones de BD de permisos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self) -> List[UserPermission]:
        """Obtener todos los permisos del sistema"""
        return self.db.query(UserPermission).all()
    
    def find_by_module(self) -> dict:
        """Obtener permisos agrupados por módulo (generados desde UserPermission)"""
        # Como UserPermission es basado en booleanos, generamos una estructura
        # de permisos del sistema
        permissions_by_module = {
            "dashboard": [
                {"id": 1, "name": "Acceder al Dashboard", "code": "can_access_dashboard"}
            ],
            "inventory": [
                {"id": 2, "name": "Acceder al Inventario", "code": "can_access_inventory"}
            ],
            "products": [
                {"id": 3, "name": "Acceder a Productos", "code": "can_access_products"}
            ],
            "menu": [
                {"id": 4, "name": "Acceder al Menú", "code": "can_access_menu"}
            ],
            "tables": [
                {"id": 5, "name": "Acceder a Mesas", "code": "can_access_tables"}
            ],
            "orders": [
                {"id": 6, "name": "Acceder a Órdenes", "code": "can_access_orders"}
            ],
            "users": [
                {"id": 7, "name": "Acceder a Usuarios", "code": "can_access_users"}
            ],
            "configuration": [
                {"id": 8, "name": "Acceder a Configuración", "code": "can_access_configuration"}
            ],
            "reports": [
                {"id": 9, "name": "Acceder a Reportes", "code": "can_access_reports"}
            ]
        }
        
        return permissions_by_module
    
    def find_by_user_id(self, user_id: int) -> Optional[UserPermission]:
        """Buscar permisos de un usuario"""
        return self.db.query(UserPermission).filter(
            UserPermission.user_id == user_id
        ).first()

