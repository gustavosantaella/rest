"""
Repositorio de cuentas por pagar - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.account_payable import AccountPayable


class AccountsPayableRepository:
    """Repositorio para operaciones de BD de cuentas por pagar"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self, business_id: int, skip: int = 0, limit: int = 100) -> List[AccountPayable]:
        """Obtener todas las cuentas por pagar de un negocio"""
        return self.db.query(AccountPayable).filter(
            AccountPayable.business_id == business_id,
            AccountPayable.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def find_by_id(self, account_id: int, business_id: int) -> Optional[AccountPayable]:
        """Buscar cuenta por pagar por ID"""
        return self.db.query(AccountPayable).filter(
            AccountPayable.id == account_id,
            AccountPayable.business_id == business_id,
            AccountPayable.deleted_at.is_(None)
        ).first()
    
    def create(self, account_data: dict) -> AccountPayable:
        """Crear nueva cuenta por pagar"""
        account = AccountPayable(**account_data)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def update(self, account: AccountPayable, update_data: dict) -> AccountPayable:
        """Actualizar cuenta por pagar"""
        for field, value in update_data.items():
            setattr(account, field, value)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def soft_delete(self, account: AccountPayable) -> None:
        """Eliminar cuenta por pagar (soft delete)"""
        account.deleted_at = datetime.now()
        self.db.commit()
    
    def create_payment(self, payment_data: dict):
        """Crear pago de cuenta por pagar"""
        from ...models.account_payable import AccountPayablePayment
        
        if 'payment_date' not in payment_data or payment_data['payment_date'] is None:
            payment_data['payment_date'] = datetime.now()
        
        payment = AccountPayablePayment(**payment_data)
        self.db.add(payment)
        self.db.flush()
        return payment
    
    def update_account_status(self, account: AccountPayable):
        """Actualizar estado de la cuenta basado en pagos"""
        from ...models.account_payable import AccountStatus
        
        self.db.refresh(account)
        
        # Calcular total pagado
        total_paid = sum(p.amount for p in account.payments)
        account.amount_paid = total_paid
        account.amount_pending = account.amount - total_paid
        
        # Actualizar estado
        if account.amount_pending <= 0.01:
            account.status = AccountStatus.PAID
            if not account.paid_date:
                account.paid_date = datetime.now()
        elif total_paid > 0:
            account.status = AccountStatus.PARTIAL
        else:
            account.status = AccountStatus.PENDING
        
        self.db.commit()
        self.db.refresh(account)

