"""
Repositorio de cuentas por cobrar - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.account_receivable import AccountReceivable


class AccountsReceivableRepository:
    """Repositorio para operaciones de BD de cuentas por cobrar"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int, skip: int = 0, limit: int = 100) -> List[AccountReceivable]:
        """Obtener todas las cuentas por cobrar de un negocio"""
        return self.db.query(AccountReceivable).filter(
            AccountReceivable.business_id == business_id,
            AccountReceivable.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def find_by_id(self, account_id: int, business_id: int) -> Optional[AccountReceivable]:
        """Buscar cuenta por cobrar por ID"""
        return self.db.query(AccountReceivable).filter(
            AccountReceivable.id == account_id,
            AccountReceivable.business_id == business_id,
            AccountReceivable.deleted_at.is_(None)
        ).first()
    
    def create(self, account_data: dict) -> AccountReceivable:
        """Crear nueva cuenta por cobrar"""
        account = AccountReceivable(**account_data)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def update(self, account: AccountReceivable, update_data: dict) -> AccountReceivable:
        """Actualizar cuenta por cobrar"""
        for field, value in update_data.items():
            setattr(account, field, value)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def soft_delete(self, account: AccountReceivable) -> None:
        """Eliminar cuenta por cobrar (soft delete)"""
        account.deleted_at = datetime.now()
        self.db.commit()

