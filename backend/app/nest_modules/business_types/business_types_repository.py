"""
Repositorio de tipos de negocios
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from ...models.business_type import BusinessType


class BusinessTypesRepository:
    """Repositorio para operaciones de base de datos de tipos de negocios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[BusinessType]:
        """Obtener todos los tipos de negocios activos"""
        return self.db.query(BusinessType).filter(
            BusinessType.is_active == True
        ).all()
    
    def get_by_id(self, business_type_id: int) -> Optional[BusinessType]:
        """Obtener tipo de negocio por ID"""
        return self.db.query(BusinessType).filter(
            BusinessType.id == business_type_id
        ).first()
    
    def get_by_slug(self, slug: str) -> Optional[BusinessType]:
        """Obtener tipo de negocio por slug"""
        return self.db.query(BusinessType).filter(
            BusinessType.slug == slug
        ).first()
    
    def create(self, business_type_data: dict) -> BusinessType:
        """Crear nuevo tipo de negocio"""
        business_type = BusinessType(**business_type_data)
        self.db.add(business_type)
        self.db.commit()
        self.db.refresh(business_type)
        return business_type
    
    def update(self, business_type_id: int, update_data: dict) -> Optional[BusinessType]:
        """Actualizar tipo de negocio"""
        business_type = self.get_by_id(business_type_id)
        if not business_type:
            return None
        
        for field, value in update_data.items():
            setattr(business_type, field, value)
        
        self.db.commit()
        self.db.refresh(business_type)
        return business_type
    
    def delete(self, business_type_id: int) -> bool:
        """Eliminar tipo de negocio (soft delete)"""
        business_type = self.get_by_id(business_type_id)
        if not business_type:
            return False
        
        business_type.is_active = False
        self.db.commit()
        return True

