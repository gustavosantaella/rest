"""
Controlador de cuentas por pagar usando PyNest
"""
from nest.core import Controller, Get, Depends
from sqlalchemy.orm import Session
from typing import List
from .accounts_payable_service import AccountsPayableService
from ...core.database import get_db
from ...models.user import User
from ...utils.dependencies import get_current_user


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
    ):
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

