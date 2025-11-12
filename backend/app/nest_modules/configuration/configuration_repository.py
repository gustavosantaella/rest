"""
Repositorio de configuración - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ...models.configuration import BusinessConfiguration, Partner


class ConfigurationRepository:
    """Repositorio para operaciones de BD de configuración"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_business_id(self, business_id: int) -> Optional[BusinessConfiguration]:
        """Buscar configuración de un negocio"""
        return self.db.query(BusinessConfiguration).filter(
            BusinessConfiguration.id == business_id
        ).first()
    
    def find_first(self) -> Optional[BusinessConfiguration]:
        """Obtener la primera configuración (para compatibilidad)"""
        return self.db.query(BusinessConfiguration).first()
    
    def create(self, config_data: dict) -> BusinessConfiguration:
        """Crear nueva configuración"""
        config = BusinessConfiguration(**config_data)
        self.db.add(config)
        self.db.commit()
        self.db.refresh(config)
        return config
    
    def update(self, config: BusinessConfiguration, update_data: dict) -> BusinessConfiguration:
        """Actualizar configuración"""
        for field, value in update_data.items():
            setattr(config, field, value)
        self.db.commit()
        self.db.refresh(config)
        return config


class PartnerRepository:
    """Repositorio para operaciones de BD de socios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int) -> List[Partner]:
        """Obtener todos los socios de un negocio"""
        return self.db.query(Partner).filter(
            Partner.business_config_id == business_id
        ).all()
    
    def find_by_id(self, partner_id: int, business_id: int) -> Optional[Partner]:
        """Buscar socio por ID"""
        return self.db.query(Partner).filter(
            Partner.id == partner_id,
            Partner.business_config_id == business_id
        ).first()
    
    def create(self, partner_data: dict) -> Partner:
        """Crear nuevo socio"""
        partner = Partner(**partner_data)
        self.db.add(partner)
        self.db.commit()
        self.db.refresh(partner)
        return partner
    
    def update(self, partner: Partner, update_data: dict) -> Partner:
        """Actualizar socio"""
        for field, value in update_data.items():
            setattr(partner, field, value)
        self.db.commit()
        self.db.refresh(partner)
        return partner
    
    def delete(self, partner: Partner) -> None:
        """Eliminar socio"""
        self.db.delete(partner)
        self.db.commit()

