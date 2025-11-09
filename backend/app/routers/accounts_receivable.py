from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.account_receivable import AccountReceivable, AccountReceivablePayment, AccountStatus
from ..models.customer import Customer
from ..models.user import User
from ..schemas.account_receivable import (
    AccountReceivableResponse,
    AccountReceivableCreate,
    AccountReceivableUpdate,
    AccountReceivablePaymentCreate,
    AccountReceivablePaymentResponse
)
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/accounts-receivable", tags=["accounts-receivable"])


def update_account_status(account: AccountReceivable):
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


@router.get("/", response_model=List[AccountReceivableResponse])
def read_accounts_receivable(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener lista de cuentas por cobrar"""
    query = db.query(AccountReceivable).options(
        joinedload(AccountReceivable.payments),
        joinedload(AccountReceivable.customer)
    ).filter(
        AccountReceivable.business_id == current_user.business_id,
        AccountReceivable.deleted_at.is_(None)
    )
    
    if status:
        query = query.filter(AccountReceivable.status == status)
    
    accounts = query.order_by(AccountReceivable.due_date.asc()).offset(skip).limit(limit).all()
    
    # Agregar nombre del cliente
    result = []
    for account in accounts:
        account_dict = AccountReceivableResponse.from_orm(account).model_dump()
        if account.customer:
            account_dict['customer_name'] = f"{account.customer.nombre} {account.customer.apellido or ''}".strip()
        result.append(account_dict)
    
    return result


@router.post("/", response_model=AccountReceivableResponse, status_code=status.HTTP_201_CREATED)
def create_account_receivable(
    account_data: AccountReceivableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crear una nueva cuenta por cobrar"""
    
    new_account = AccountReceivable(
        business_id=current_user.business_id,
        customer_id=account_data.customer_id,
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


@router.get("/{account_id}", response_model=AccountReceivableResponse)
def read_account_receivable(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener una cuenta por cobrar por ID"""
    account = (
        db.query(AccountReceivable)
        .options(joinedload(AccountReceivable.payments))
        .filter(
            AccountReceivable.id == account_id,
            AccountReceivable.business_id == current_user.business_id,
            AccountReceivable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por cobrar no encontrada"
        )
    return account


@router.put("/{account_id}", response_model=AccountReceivableResponse)
def update_account_receivable(
    account_id: int,
    account_update: AccountReceivableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualizar una cuenta por cobrar"""
    account = (
        db.query(AccountReceivable)
        .filter(
            AccountReceivable.id == account_id,
            AccountReceivable.business_id == current_user.business_id,
            AccountReceivable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por cobrar no encontrada"
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
def delete_account_receivable(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Eliminar una cuenta por cobrar (soft delete)"""
    account = (
        db.query(AccountReceivable)
        .filter(
            AccountReceivable.id == account_id,
            AccountReceivable.business_id == current_user.business_id,
            AccountReceivable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por cobrar no encontrada"
        )
    
    account.deleted_at = datetime.now()
    db.commit()
    return None


@router.post("/{account_id}/payments", response_model=AccountReceivablePaymentResponse, status_code=status.HTTP_201_CREATED)
def add_payment_to_account(
    account_id: int,
    payment_data: AccountReceivablePaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Agregar un pago a una cuenta por cobrar"""
    account = (
        db.query(AccountReceivable)
        .filter(
            AccountReceivable.id == account_id,
            AccountReceivable.business_id == current_user.business_id,
            AccountReceivable.deleted_at.is_(None)
        )
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta por cobrar no encontrada"
        )
    
    # Verificar que no se pague más de lo pendiente
    if payment_data.amount > account.amount_pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El monto del pago (${payment_data.amount}) excede el monto pendiente (${account.amount_pending})"
        )
    
    # Crear pago
    new_payment = AccountReceivablePayment(
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
def get_receivable_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener resumen de cuentas por cobrar"""
    accounts = db.query(AccountReceivable).filter(
        AccountReceivable.business_id == current_user.business_id,
        AccountReceivable.deleted_at.is_(None)
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

