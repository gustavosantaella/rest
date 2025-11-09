from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.account_payable import AccountPayable, AccountPayablePayment, AccountStatus
from ..models.user import User
from ..schemas.account_payable import (
    AccountPayableResponse,
    AccountPayableCreate,
    AccountPayableUpdate,
    AccountPayablePaymentCreate,
    AccountPayablePaymentResponse
)
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/accounts-payable", tags=["accounts-payable"])


def update_account_status(account: AccountPayable):
    """Actualiza el estado de la cuenta basado en pagos y fecha"""
    if account.amount_pending <= 0:
        account.status = AccountStatus.PAID
        if not account.paid_date:
            account.paid_date = datetime.now()
    elif account.amount_paid > 0:
        account.status = AccountStatus.PARTIAL
    elif datetime.now() > account.due_date:
        account.status = AccountStatus.OVERDUE
    else:
        account.status = AccountStatus.PENDING


@router.get("/", response_model=List[AccountPayableResponse])
def read_accounts_payable(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener lista de cuentas por pagar"""
    query = db.query(AccountPayable).options(
        joinedload(AccountPayable.payments)
    ).filter(
        AccountPayable.business_id == current_user.business_id,
        AccountPayable.deleted_at.is_(None)
    )
    
    if status:
        query = query.filter(AccountPayable.status == status)
    
    accounts = query.order_by(AccountPayable.due_date.asc()).offset(skip).limit(limit).all()
    
    return accounts


@router.post("/", response_model=AccountPayableResponse, status_code=status.HTTP_201_CREATED)
def create_account_payable(
    account_data: AccountPayableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crear una nueva cuenta por pagar"""
    
    new_account = AccountPayable(
        business_id=current_user.business_id,
        supplier_name=account_data.supplier_name,
        supplier_phone=account_data.supplier_phone,
        supplier_email=account_data.supplier_email,
        invoice_number=account_data.invoice_number,
        description=account_data.description,
        amount=account_data.amount,
        amount_paid=0.0,
        amount_pending=account_data.amount,
        due_date=account_data.due_date,
        notes=account_data.notes,
        status=AccountStatus.PENDING
    )
    
    # Verificar si ya está vencida
    if datetime.now() > new_account.due_date:
        new_account.status = AccountStatus.OVERDUE
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return new_account


@router.get("/{account_id}", response_model=AccountPayableResponse)
def read_account_payable(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener una cuenta por pagar por ID"""
    account = (
        db.query(AccountPayable)
        .options(joinedload(AccountPayable.payments))
        .filter(
            AccountPayable.id == account_id,
            AccountPayable.business_id == current_user.business_id,
            AccountPayable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por pagar no encontrada"
        )
    return account


@router.put("/{account_id}", response_model=AccountPayableResponse)
def update_account_payable(
    account_id: int,
    account_update: AccountPayableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualizar una cuenta por pagar"""
    account = (
        db.query(AccountPayable)
        .filter(
            AccountPayable.id == account_id,
            AccountPayable.business_id == current_user.business_id,
            AccountPayable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por pagar no encontrada"
        )
    
    update_data = account_update.model_dump(exclude_unset=True)
    
    # Si se actualiza el monto, recalcular pendiente
    if "amount" in update_data:
        account.amount_pending = update_data["amount"] - account.amount_paid
    
    for field, value in update_data.items():
        setattr(account, field, value)
    
    update_account_status(account)
    
    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account_payable(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Eliminar una cuenta por pagar (soft delete)"""
    account = (
        db.query(AccountPayable)
        .filter(
            AccountPayable.id == account_id,
            AccountPayable.business_id == current_user.business_id,
            AccountPayable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por pagar no encontrada"
        )
    
    account.deleted_at = datetime.now()
    db.commit()
    return None


@router.post("/{account_id}/payments", response_model=AccountPayablePaymentResponse, status_code=status.HTTP_201_CREATED)
def add_payment_to_account(
    account_id: int,
    payment_data: AccountPayablePaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Agregar un pago a una cuenta por pagar"""
    account = (
        db.query(AccountPayable)
        .filter(
            AccountPayable.id == account_id,
            AccountPayable.business_id == current_user.business_id,
            AccountPayable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por pagar no encontrada"
        )
    
    # Verificar que no se pague más de lo pendiente
    if payment_data.amount > account.amount_pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El monto del pago (${payment_data.amount}) excede el monto pendiente (${account.amount_pending})"
        )
    
    # Crear pago
    new_payment = AccountPayablePayment(
        account_id=account_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        reference=payment_data.reference,
        notes=payment_data.notes
    )
    
    # Actualizar cuenta
    account.amount_paid += payment_data.amount
    account.amount_pending -= payment_data.amount
    
    update_account_status(account)
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    
    return new_payment


@router.get("/summary/stats")
def get_payable_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener resumen de cuentas por pagar"""
    accounts = db.query(AccountPayable).filter(
        AccountPayable.business_id == current_user.business_id,
        AccountPayable.deleted_at.is_(None)
    ).all()
    
    total_pending = sum(acc.amount_pending for acc in accounts if acc.status in [AccountStatus.PENDING, AccountStatus.PARTIAL, AccountStatus.OVERDUE])
    total_overdue = sum(acc.amount_pending for acc in accounts if acc.status == AccountStatus.OVERDUE)
    count_pending = len([acc for acc in accounts if acc.status in [AccountStatus.PENDING, AccountStatus.PARTIAL]])
    count_overdue = len([acc for acc in accounts if acc.status == AccountStatus.OVERDUE])
    
    return {
        "total_pending": total_pending,
        "total_overdue": total_overdue,
        "count_pending": count_pending,
        "count_overdue": count_overdue
    }

