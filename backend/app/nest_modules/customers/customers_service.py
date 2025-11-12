"""
Servicio de clientes usando PyNest
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from ...models.customer import Customer
from ...schemas.customer import CustomerCreate, CustomerUpdate


@Injectable
class CustomersService:
    """Servicio para manejo de clientes"""
    
    def __init__(self):
        pass
    
    def create_customer(
        self,
        customer_data: CustomerCreate,
        business_id: int,
        db: Session
    ) -> Customer:
        """Crear nuevo cliente"""
        # Verificar DNI duplicado si se proporciona
        if customer_data.dni:
            existing = db.query(Customer).filter(
                Customer.dni == customer_data.dni,
                Customer.business_id == business_id,
                Customer.deleted_at.is_(None)
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un cliente con este DNI en tu negocio"
                )
        
        # Crear cliente
        new_customer = Customer(
            business_id=business_id,
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
    
    def get_customers(
        self,
        business_id: int,
        skip: int,
        limit: int,
        search: Optional[str],
        db: Session
    ) -> List[Customer]:
        """Obtener lista de clientes"""
        query = db.query(Customer).filter(
            Customer.business_id == business_id,
            Customer.deleted_at.is_(None)
        )
        
        # Búsqueda por nombre, apellido, dni, teléfono o correo
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Customer.nombre.ilike(search_filter),
                    Customer.apellido.ilike(search_filter),
                    Customer.dni.ilike(search_filter),
                    Customer.telefono.ilike(search_filter),
                    Customer.correo.ilike(search_filter)
                )
            )
        
        return query.order_by(Customer.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_customer_by_id(
        self,
        customer_id: int,
        business_id: int,
        db: Session
    ) -> Customer:
        """Obtener cliente por ID"""
        customer = db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.business_id == business_id,
            Customer.deleted_at.is_(None)
        ).first()
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        return customer
    
    def update_customer(
        self,
        customer_id: int,
        customer_update: CustomerUpdate,
        business_id: int,
        db: Session
    ) -> Customer:
        """Actualizar cliente"""
        customer = self.get_customer_by_id(customer_id, business_id, db)
        
        # Verificar DNI duplicado si se está actualizando
        if customer_update.dni and customer_update.dni != customer.dni:
            existing = db.query(Customer).filter(
                Customer.dni == customer_update.dni,
                Customer.business_id == business_id,
                Customer.id != customer_id,
                Customer.deleted_at.is_(None)
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otro cliente con este DNI en tu negocio"
                )
        
        update_data = customer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        db.commit()
        db.refresh(customer)
        return customer
    
    def delete_customer(self, customer_id: int, business_id: int, db: Session) -> None:
        """Eliminar cliente (soft delete)"""
        customer = self.get_customer_by_id(customer_id, business_id, db)
        customer.deleted_at = datetime.now()
        db.commit()

