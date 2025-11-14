"""
Servicio de cuentas por cobrar usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from .accounts_receivable_repository import AccountsReceivableRepository
from ...schemas.account_receivable import (
    AccountReceivableCreate, AccountReceivableUpdate,
    AccountReceivablePaymentCreate, AccountReceivablePaymentResponse,
    AccountReceivableResponse
)
from ...models.account_receivable import AccountStatus
from ...models.order import OrderStatus


@Injectable
class AccountsReceivableService:
    """Servicio para lógica de negocio de cuentas por cobrar"""
    
    def __init__(self):
        pass
    
    def get_accounts(self, business_id: int, skip: int, limit: int, db: Session):
        """Obtener lista de cuentas por cobrar"""
        repo = AccountsReceivableRepository(db)
        accounts = repo.find_all(business_id, skip, limit)
        # Serializar con Pydantic para asegurar validación correcta
        return [AccountReceivableResponse.model_validate(acc, from_attributes=True) for acc in accounts]
    
    def get_summary(self, business_id: int, db: Session):
        """Obtener resumen de cuentas por cobrar"""
        repo = AccountsReceivableRepository(db)
        accounts = repo.find_all(business_id, 0, 10000)
        
        # Calcular montos por estado
        pending_accounts = [acc for acc in accounts if acc.status == "pending"]
        overdue_accounts = [acc for acc in accounts if acc.status == "overdue"]
        
        # Asegurar que todos los valores sean números flotantes válidos
        total_pending = float(sum(acc.amount_pending for acc in accounts) or 0)
        total_overdue = float(sum(acc.amount for acc in overdue_accounts) or 0)
        count_pending = len(pending_accounts)
        count_overdue = len(overdue_accounts)
        
        return {
            "total_pending": total_pending,
            "total_overdue": total_overdue,
            "count_pending": count_pending,
            "count_overdue": count_overdue
        }
    
    def get_summary_stats(self, business_id: int, db: Session):
        """Obtener estadísticas detalladas de cuentas por cobrar"""
        repo = AccountsReceivableRepository(db)
        accounts = repo.find_all(business_id, 0, 10000)
        
        total = sum(acc.amount for acc in accounts)
        pending = sum(acc.amount for acc in accounts if acc.status == "pending")
        paid = sum(acc.amount for acc in accounts if acc.status == "paid")
        overdue = sum(acc.amount for acc in accounts if acc.status == "overdue")
        
        return {
            "total_amount": total,
            "pending_amount": pending,
            "paid_amount": paid,
            "overdue_amount": overdue,
            "total_count": len(accounts),
            "pending_count": len([a for a in accounts if a.status == "pending"]),
            "paid_count": len([a for a in accounts if a.status == "paid"]),
            "overdue_count": len([a for a in accounts if a.status == "overdue"])
        }
    
    def create_account(self, account_data: AccountReceivableCreate, business_id: int, db: Session):
        """Crear nueva cuenta por cobrar"""
        repo = AccountsReceivableRepository(db)
        
        account_dict = account_data.model_dump()
        account_dict['business_id'] = business_id
        
        # Calcular amount_pending automáticamente si no se proporciona
        if 'amount_pending' not in account_dict or account_dict['amount_pending'] is None:
            amount = account_dict.get('amount', 0)
            amount_paid = account_dict.get('amount_paid', 0)
            account_dict['amount_pending'] = amount - amount_paid
        
        return repo.create(account_dict)
    
    def update_account(
        self,
        account_id: int,
        account_update: AccountReceivableUpdate,
        business_id: int,
        db: Session
    ):
        """Actualizar cuenta por cobrar"""
        repo = AccountsReceivableRepository(db)
        
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta por cobrar no encontrada"
            )
        
        update_data = account_update.model_dump(exclude_unset=True)
        return repo.update(account, update_data)
    
    def delete_account(self, account_id: int, business_id: int, db: Session):
        """Eliminar cuenta por cobrar"""
        repo = AccountsReceivableRepository(db)
        
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta por cobrar no encontrada"
            )
        
        repo.soft_delete(account)
    
    def add_payment(
        self,
        account_id: int,
        payment_data: AccountReceivablePaymentCreate,
        business_id: int,
        db: Session
    ) -> AccountReceivablePaymentResponse:
        """Agregar pago a una cuenta por cobrar"""
        repo = AccountsReceivableRepository(db)
        
        # Buscar la cuenta
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta por cobrar no encontrada"
            )
        
        # Validar que el pago no exceda el monto pendiente
        if payment_data.amount > account.amount_pending:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El pago (${payment_data.amount:.2f}) excede el monto pendiente (${account.amount_pending:.2f})"
            )
        
        # Crear el pago
        payment_dict = payment_data.model_dump()
        payment_dict['account_id'] = account.id
        payment = repo.create_payment(payment_dict)
        
        # Actualizar estado de la cuenta
        repo.update_account_status(account)
        
        # Refrescar la cuenta para obtener el estado actualizado
        db.refresh(account)
        
        # Verificar si la cuenta está pagada (comparar tanto enum como string)
        is_paid = (
            account.status == AccountStatus.PAID or 
            str(account.status) == AccountStatus.PAID.value or
            account.status == AccountStatus.PAID.value
        )
        
        # Si la cuenta está pagada y tiene una orden relacionada, actualizar la orden
        if is_paid and account.order_id:
            self._update_related_order(account.order_id, business_id, db)
        
        # Asegurar que payment_date tenga un valor antes de serializar
        if payment.payment_date is None:
            payment.payment_date = payment.created_at if payment.created_at else datetime.now()
            db.commit()
            db.refresh(payment)
        
        return AccountReceivablePaymentResponse.model_validate(payment, from_attributes=True)
    
    def _update_related_order(self, order_id: int, business_id: int, db: Session):
        """Actualizar orden relacionada cuando la cuenta por cobrar se marca como pagada"""
        from ...nest_modules.orders.orders_repository import OrderRepository
        from ...models.order import OrderStatus
        
        order_repo = OrderRepository(db)
        order = order_repo.find_by_id(order_id, business_id)
        
        if order:
            # Marcar orden como pagada y completada
            update_data = {
                'payment_status': 'paid',
                'status': OrderStatus.COMPLETED.value,
                'paid_at': datetime.now()
            }
            order_repo.update(order, update_data)
            db.refresh(order)

