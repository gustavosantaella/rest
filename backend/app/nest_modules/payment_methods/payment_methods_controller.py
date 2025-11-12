"""
Controlador de métodos de pago usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .payment_methods_service import PaymentMethodsService
from ...core.database import get_db
from ...models.user import User
from ...schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse
from ...utils.dependencies import get_current_user, get_current_active_admin


@Controller("api/payment-methods")
class PaymentMethodsController:
    """Controlador para rutas de métodos de pago"""
    
    def __init__(self, service: PaymentMethodsService):
        self.service = service
    
    @Get("/active")
    def get_active_payment_methods(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[PaymentMethodResponse]:
        """Obtener solo los métodos de pago activos"""
        return self.service.get_active_payment_methods(
            current_user.business_id,
            db
        )
    
    @Get("/")
    def get_payment_methods(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[PaymentMethodResponse]:
        """Obtener métodos de pago del negocio"""
        return self.service.get_payment_methods(
            current_user.business_id,
            skip,
            limit,
            db
        )
    
    @Get("/{payment_method_id}")
    def get_payment_method(
        self,
        payment_method_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> PaymentMethodResponse:
        """Obtener método de pago por ID"""
        return self.service.get_payment_method_by_id(
            payment_method_id,
            current_user.business_id,
            db
        )
    
    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_payment_method(
        self,
        payment_method: PaymentMethodCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> PaymentMethodResponse:
        """Crear nuevo método de pago"""
        return self.service.create_payment_method(
            payment_method,
            current_user.business_id,
            db
        )
    
    @Put("/{payment_method_id}")
    def update_payment_method(
        self,
        payment_method_id: int,
        payment_method_update: PaymentMethodUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> PaymentMethodResponse:
        """Actualizar método de pago"""
        return self.service.update_payment_method(
            payment_method_id,
            payment_method_update,
            current_user.business_id,
            db
        )
    
    @Delete("/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_payment_method(
        self,
        payment_method_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ):
        """Eliminar método de pago"""
        self.service.delete_payment_method(
            payment_method_id,
            current_user.business_id,
            db
        )
        return None

