from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import PaymentMethod
from app.models.user import User
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse
from app.utils.dependencies import get_current_active_admin, get_current_user

router = APIRouter(prefix="/payment-methods", tags=["payment-methods"])

@router.get("/", response_model=List[PaymentMethodResponse])
def read_payment_methods(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener todos los métodos de pago del negocio del usuario (no eliminados)"""
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no asociado a ningún negocio"
        )
    
    payment_methods = db.query(PaymentMethod).filter(
        PaymentMethod.business_id == current_user.business_id,
        PaymentMethod.deleted_at.is_(None)  # Solo métodos no eliminados
    ).offset(skip).limit(limit).all()
    return payment_methods

@router.get("/active", response_model=List[PaymentMethodResponse])
def read_active_payment_methods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener solo los métodos de pago activos del negocio (no eliminados)"""
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no asociado a ningún negocio"
        )
    
    payment_methods = db.query(PaymentMethod).filter(
        PaymentMethod.business_id == current_user.business_id,
        PaymentMethod.is_active == True,
        PaymentMethod.deleted_at.is_(None)  # Solo métodos no eliminados
    ).all()
    return payment_methods

@router.get("/{payment_method_id}", response_model=PaymentMethodResponse)
def read_payment_method(
    payment_method_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener un método de pago por ID del negocio del usuario (no eliminado)"""
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no asociado a ningún negocio"
        )
    
    payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.id == payment_method_id,
        PaymentMethod.business_id == current_user.business_id,
        PaymentMethod.deleted_at.is_(None)  # Solo métodos no eliminados
    ).first()
    if not payment_method:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    return payment_method

@router.post("/", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment_method(
    payment_method: PaymentMethodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Crear un nuevo método de pago para el negocio del usuario (solo Admin)"""
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no asociado a ningún negocio"
        )
    
    # Crear el método de pago asociado al negocio del usuario
    payment_data = payment_method.dict()
    payment_data['business_id'] = current_user.business_id
    
    db_payment_method = PaymentMethod(**payment_data)
    db.add(db_payment_method)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method

@router.put("/{payment_method_id}", response_model=PaymentMethodResponse)
def update_payment_method(
    payment_method_id: int,
    payment_method: PaymentMethodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Actualizar un método de pago del negocio del usuario (solo Admin)"""
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no asociado a ningún negocio"
        )
    
    db_payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.id == payment_method_id,
        PaymentMethod.business_id == current_user.business_id,
        PaymentMethod.deleted_at.is_(None)  # Solo métodos no eliminados
    ).first()
    if not db_payment_method:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    
    update_data = payment_method.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_payment_method, field, value)
    
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method

@router.delete("/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_method(
    payment_method_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Eliminar un método de pago del negocio del usuario (solo Admin) - Soft delete"""
    from datetime import datetime
    
    if not current_user.business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no asociado a ningún negocio"
        )
    
    db_payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.id == payment_method_id,
        PaymentMethod.business_id == current_user.business_id,
        PaymentMethod.deleted_at.is_(None)  # Solo métodos no eliminados
    ).first()
    if not db_payment_method:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    
    # Soft delete: marcar como eliminado con timestamp
    db_payment_method.deleted_at = datetime.now()
    db.commit()
    return None

