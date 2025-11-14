"""
Servicio de cuentas por pagar usando PyNest - Lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from .accounts_payable_repository import AccountsPayableRepository
from ...schemas.account_payable import (
    AccountPayableCreate, AccountPayableUpdate,
    AccountPayablePaymentCreate, AccountPayablePaymentResponse
)


@Injectable
class AccountsPayableService:
    """Servicio para lógica de negocio de cuentas por pagar"""
    
    def __init__(self, accounting_integration=None):
        self.accounting_integration = accounting_integration
    
    def get_accounts(self, business_id: int, skip: int, limit: int, db: Session):
        """Obtener lista de cuentas por pagar"""
        repo = AccountsPayableRepository(db)
        return repo.find_all(business_id, skip, limit)
    
    def get_summary(self, business_id: int, db: Session):
        """Obtener resumen de cuentas por pagar"""
        repo = AccountsPayableRepository(db)
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
        """Obtener estadísticas detalladas de cuentas por pagar"""
        repo = AccountsPayableRepository(db)
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
    
    def create_account(self, account_data: AccountPayableCreate, business_id: int, db: Session):
        """Crear nueva cuenta por pagar"""
        repo = AccountsPayableRepository(db)
        
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
        account_update: AccountPayableUpdate,
        business_id: int,
        db: Session
    ):
        """Actualizar cuenta por pagar"""
        repo = AccountsPayableRepository(db)
        
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta por pagar no encontrada"
            )
        
        update_data = account_update.model_dump(exclude_unset=True)
        return repo.update(account, update_data)
    
    def delete_account(self, account_id: int, business_id: int, db: Session):
        """Eliminar cuenta por pagar"""
        repo = AccountsPayableRepository(db)
        
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta por pagar no encontrada"
            )
        
        repo.soft_delete(account)
    
    def add_payment(
        self,
        account_id: int,
        payment_data: AccountPayablePaymentCreate,
        business_id: int,
        db: Session
    ) -> AccountPayablePaymentResponse:
        """Agregar pago a una cuenta por pagar"""
        repo = AccountsPayableRepository(db)
        
        # Buscar la cuenta
        account = repo.find_by_id(account_id, business_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta por pagar no encontrada"
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
        
        # Generar asiento contable automático para el pago
        if self.accounting_integration:
            try:
                user_id = 1  # TODO: Obtener del contexto de autenticación
                self.accounting_integration.create_payable_payment_entry(
                    account, payment, business_id, user_id, db
                )
            except Exception as e:
                # No fallar el pago si falla el asiento contable
                print(f"Error al crear asiento contable automático: {str(e)}")
        
        # Asegurar que payment_date tenga un valor
        if payment.payment_date is None:
            payment.payment_date = payment.created_at if payment.created_at else datetime.now()
            db.commit()
            db.refresh(payment)
        
        return AccountPayablePaymentResponse.model_validate(payment, from_attributes=True)

