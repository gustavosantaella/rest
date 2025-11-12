"""
Servicio de cuentas por cobrar usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from .accounts_receivable_repository import AccountsReceivableRepository


@Injectable
class AccountsReceivableService:
    """Servicio para lógica de negocio de cuentas por cobrar"""
    
    def __init__(self):
        pass
    
    def get_accounts(self, business_id: int, skip: int, limit: int, db: Session):
        """Obtener lista de cuentas por cobrar"""
        repo = AccountsReceivableRepository(db)
        return repo.find_all(business_id, skip, limit)
    
    def get_summary(self, business_id: int, db: Session):
        """Obtener resumen de cuentas por cobrar"""
        repo = AccountsReceivableRepository(db)
        accounts = repo.find_all(business_id, 0, 10000)  # Obtener todas para el resumen
        
        total = sum(acc.amount for acc in accounts)
        pending = sum(acc.amount for acc in accounts if acc.status == "pending")
        paid = sum(acc.amount for acc in accounts if acc.status == "paid")
        
        return {
            "total": total,
            "pending": pending,
            "paid": paid,
            "count": len(accounts)
        }

