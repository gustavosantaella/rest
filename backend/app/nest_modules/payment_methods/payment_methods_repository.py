"""
Repositorio de métodos de pago - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.payment_method import PaymentMethod


class PaymentMethodsRepository:
    """Repositorio para operaciones de BD de métodos de pago"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int, skip: int = 0, limit: int = 100) -> List[PaymentMethod]:
        """Obtener todos los métodos de pago de un negocio"""
        return self.db.query(PaymentMethod).filter(
            PaymentMethod.business_id == business_id,
            PaymentMethod.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def find_active(self, business_id: int) -> List[PaymentMethod]:
        """Obtener solo los métodos de pago activos"""
        return self.db.query(PaymentMethod).filter(
            PaymentMethod.business_id == business_id,
            PaymentMethod.is_active == True,
            PaymentMethod.deleted_at.is_(None)
        ).all()
    
    def find_by_id(self, payment_method_id: int, business_id: int) -> Optional[PaymentMethod]:
        """Buscar método de pago por ID"""
        return self.db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_method_id,
            PaymentMethod.business_id == business_id,
            PaymentMethod.deleted_at.is_(None)
        ).first()
    
    def create(self, payment_method_data: dict) -> PaymentMethod:
        """Crear nuevo método de pago"""
        payment_method = PaymentMethod(**payment_method_data)
        self.db.add(payment_method)
        self.db.commit()
        self.db.refresh(payment_method)
        return payment_method
    
    def update(self, payment_method: PaymentMethod, update_data: dict) -> PaymentMethod:
        """Actualizar método de pago"""
        for field, value in update_data.items():
            setattr(payment_method, field, value)
        self.db.commit()
        self.db.refresh(payment_method)
        return payment_method
    
    def soft_delete(self, payment_method: PaymentMethod) -> None:
        """Eliminar método de pago (soft delete)"""
        payment_method.deleted_at = datetime.now()
        self.db.commit()

