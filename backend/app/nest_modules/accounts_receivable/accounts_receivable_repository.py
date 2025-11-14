"""
Repositorio de cuentas por cobrar - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.account_receivable import AccountReceivable, AccountReceivablePayment, AccountStatus


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
    
    def create_payment(self, payment_data: dict) -> AccountReceivablePayment:
        """Crear pago de cuenta por cobrar"""
        # Asegurar que payment_date tenga un valor por defecto
        if 'payment_date' not in payment_data or payment_data['payment_date'] is None:
            payment_data['payment_date'] = datetime.now()
        
        payment = AccountReceivablePayment(**payment_data)
        self.db.add(payment)
        self.db.flush()
        return payment
    
    def update_account_status(self, account: AccountReceivable):
        """Actualizar estado de la cuenta basado en pagos"""
        # Recargar los pagos para asegurar que tenemos los datos actualizados
        self.db.refresh(account)
        
        # Calcular total pagado
        total_paid = sum(p.amount for p in account.payments)
        account.amount_paid = total_paid
        account.amount_pending = account.amount - total_paid
        
        # Actualizar estado
        if account.amount_pending <= 0.01:  # Usar tolerancia para comparaciones de float
            account.status = AccountStatus.PAID
            if not account.paid_date:
                account.paid_date = datetime.now()
        elif total_paid > 0:
            account.status = AccountStatus.PARTIAL
        else:
            account.status = AccountStatus.PENDING
        
        self.db.commit()
        self.db.refresh(account)

