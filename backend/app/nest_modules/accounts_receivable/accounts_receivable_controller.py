"""
Controlador de cuentas por cobrar usando PyNest
"""
from nest.core import Controller, Get, Depends
from sqlalchemy.orm import Session
from typing import List
from .accounts_receivable_service import AccountsReceivableService
from ...core.database import get_db
from ...models.user import User
from ...utils.dependencies import get_current_user


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
    ):
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

