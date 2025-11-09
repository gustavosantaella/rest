from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.customer import Customer
from ..models.user import User
from ..schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=List[CustomerResponse])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener lista de clientes del negocio actual"""
    query = db.query(Customer).filter(
        Customer.business_id == current_user.business_id,
        Customer.deleted_at.is_(None)  # Solo clientes no eliminados
    )
    
    # Búsqueda por nombre, apellido, dni, teléfono o correo
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Customer.nombre.ilike(search_filter)) |
            (Customer.apellido.ilike(search_filter)) |
            (Customer.dni.ilike(search_filter)) |
            (Customer.telefono.ilike(search_filter)) |
            (Customer.correo.ilike(search_filter))
        )
    
    customers = query.order_by(Customer.created_at.desc()).offset(skip).limit(limit).all()
    return customers


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Crear un nuevo cliente"""
    
    # Verificar si ya existe un cliente con el mismo DNI en este negocio (si se proporciona)
    if customer_data.dni:
        existing = (
            db.query(Customer)
            .filter(
                Customer.dni == customer_data.dni,
                Customer.business_id == current_user.business_id,
                Customer.deleted_at.is_(None)
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un cliente con este DNI en tu negocio",
            )
    
    # Crear cliente
    new_customer = Customer(
        business_id=current_user.business_id,
        nombre=customer_data.nombre,
        apellido=customer_data.apellido,
        dni=customer_data.dni,
        telefono=customer_data.telefono,
        correo=customer_data.correo,
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return new_customer


@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener un cliente por ID"""
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.business_id == current_user.business_id,
            Customer.deleted_at.is_(None)
        )
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado"
        )
    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualizar un cliente existente"""
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.business_id == current_user.business_id,
            Customer.deleted_at.is_(None)
        )
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado"
        )
    
    # Verificar DNI duplicado si se está actualizando
    if customer_update.dni and customer_update.dni != customer.dni:
        existing = (
            db.query(Customer)
            .filter(
                Customer.dni == customer_update.dni,
                Customer.business_id == current_user.business_id,
                Customer.id != customer_id,
                Customer.deleted_at.is_(None)
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro cliente con este DNI en tu negocio",
            )
    
    update_data = customer_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Eliminar un cliente (soft delete)"""
    from datetime import datetime
    
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.business_id == current_user.business_id,
            Customer.deleted_at.is_(None)
        )
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado"
        )
    
    # Soft delete: marcar como eliminado con timestamp
    customer.deleted_at = datetime.now()
    db.commit()
    return None

