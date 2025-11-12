"""
Servicio de métodos de pago usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from .payment_methods_repository import PaymentMethodsRepository
from ...schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate


@Injectable
class PaymentMethodsService:
    """Servicio para lógica de negocio de métodos de pago"""
    
    def __init__(self):
        pass
    
    def get_payment_methods(self, business_id: int, skip: int, limit: int, db: Session):
        """Obtener lista de métodos de pago"""
        repo = PaymentMethodsRepository(db)
        return repo.find_all(business_id, skip, limit)
    
    def get_active_payment_methods(self, business_id: int, db: Session):
        """Obtener solo los métodos de pago activos"""
        repo = PaymentMethodsRepository(db)
        return repo.find_active(business_id)
    
    def get_payment_method_by_id(self, payment_method_id: int, business_id: int, db: Session):
        """Obtener método de pago por ID"""
        repo = PaymentMethodsRepository(db)
        payment_method = repo.find_by_id(payment_method_id, business_id)
        
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Método de pago no encontrado"
            )
        
        return payment_method
    
    def create_payment_method(self, payment_method_data: PaymentMethodCreate, business_id: int, db: Session):
        """Crear nuevo método de pago"""
        repo = PaymentMethodsRepository(db)
        
        payment_method_dict = payment_method_data.model_dump()
        payment_method_dict['business_id'] = business_id
        
        return repo.create(payment_method_dict)
    
    def update_payment_method(
        self,
        payment_method_id: int,
        payment_method_update: PaymentMethodUpdate,
        business_id: int,
        db: Session
    ):
        """Actualizar método de pago"""
        repo = PaymentMethodsRepository(db)
        
        payment_method = repo.find_by_id(payment_method_id, business_id)
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Método de pago no encontrado"
            )
        
        update_data = payment_method_update.model_dump(exclude_unset=True)
        return repo.update(payment_method, update_data)
    
    def delete_payment_method(self, payment_method_id: int, business_id: int, db: Session):
        """Eliminar método de pago"""
        repo = PaymentMethodsRepository(db)
        
        payment_method = repo.find_by_id(payment_method_id, business_id)
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Método de pago no encontrado"
            )
        
        repo.soft_delete(payment_method)

