"""
Controlador de cuentas por pagar usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .accounts_payable_service import AccountsPayableService
from ...core.database import get_db
from ...models.user import User
from ...schemas.account_payable import (
    AccountPayableCreate,
    AccountPayableUpdate,
    AccountPayableResponse,
    AccountPayablePaymentCreate,
    AccountPayablePaymentResponse
)
from ...utils.dependencies import get_current_user, get_current_active_admin


@Controller("api/accounts-payable")
class AccountsPayableController:
    """Controlador para rutas de cuentas por pagar"""
    
    def __init__(self, service: AccountsPayableService):
        self.service = service
    
    @Get("/")
    def get_accounts_payable(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[AccountPayableResponse]:
        """Obtener cuentas por pagar"""
        return self.service.get_accounts(
            current_user.business_id,
            skip,
            limit,
            db
        )
    
    @Get("/summary")
    def get_summary(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener resumen de cuentas por pagar"""
        return self.service.get_summary(current_user.business_id, db)
    
    @Get("/summary/stats")
    def get_summary_stats(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener estadísticas detalladas de cuentas por pagar"""
        return self.service.get_summary_stats(current_user.business_id, db)
    
    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_account_payable(
        self,
        account: AccountPayableCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> AccountPayableResponse:
        """Crear nueva cuenta por pagar"""
        return self.service.create_account(
            account,
            current_user.business_id,
            db
        )
    
    @Put("/{account_id}")
    def update_account_payable(
        self,
        account_id: int,
        account_update: AccountPayableUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> AccountPayableResponse:
        """Actualizar cuenta por pagar"""
        return self.service.update_account(
            account_id,
            account_update,
            current_user.business_id,
            db
        )
    
    @Delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_account_payable(
        self,
        account_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ):
        """Eliminar cuenta por pagar"""
        self.service.delete_account(
            account_id,
            current_user.business_id,
            db
        )
        return None
    
    @Post("/{account_id}/payments", status_code=status.HTTP_201_CREATED)
    def add_payment(
        self,
        account_id: int,
        payment: AccountPayablePaymentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> AccountPayablePaymentResponse:
        """Agregar pago a una cuenta por pagar"""
        return self.service.add_payment(
            account_id, payment, current_user.business_id, db
        )

