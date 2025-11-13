"""
Controlador de cuentas por cobrar usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .accounts_receivable_service import AccountsReceivableService
from ...core.database import get_db
from ...models.user import User
from ...schemas.account_receivable import (
    AccountReceivableCreate,
    AccountReceivableUpdate,
    AccountReceivableResponse
)
from ...utils.dependencies import get_current_user, get_current_active_admin


@Controller("api/accounts-receivable")
class AccountsReceivableController:
    """Controlador para rutas de cuentas por cobrar"""
    
    def __init__(self, service: AccountsReceivableService):
        self.service = service
    
    @Get("/")
    def get_accounts_receivable(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[AccountReceivableResponse]:
        """Obtener cuentas por cobrar"""
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
        """Obtener resumen de cuentas por cobrar"""
        return self.service.get_summary(current_user.business_id, db)
    
    @Get("/summary/stats")
    def get_summary_stats(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Obtener estadísticas detalladas de cuentas por cobrar"""
        return self.service.get_summary_stats(current_user.business_id, db)
    
    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_account_receivable(
        self,
        account: AccountReceivableCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> AccountReceivableResponse:
        """Crear nueva cuenta por cobrar"""
        return self.service.create_account(
            account,
            current_user.business_id,
            db
        )
    
    @Put("/{account_id}")
    def update_account_receivable(
        self,
        account_id: int,
        account_update: AccountReceivableUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ) -> AccountReceivableResponse:
        """Actualizar cuenta por cobrar"""
        return self.service.update_account(
            account_id,
            account_update,
            current_user.business_id,
            db
        )
    
    @Delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_account_receivable(
        self,
        account_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_admin)
    ):
        """Eliminar cuenta por cobrar"""
        self.service.delete_account(
            account_id,
            current_user.business_id,
            db
        )
        return None

