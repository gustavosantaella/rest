"""
Repositorio de clientes - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from ...models.customer import Customer


class CustomerRepository:
    """Repositorio para operaciones de BD de clientes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, customer_id: int, business_id: int) -> Optional[Customer]:
        """Buscar cliente por ID en un negocio"""
        return self.db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.business_id == business_id,
            Customer.deleted_at.is_(None)
        ).first()
    
    def find_by_dni(self, dni: str, business_id: int, exclude_id: Optional[int] = None) -> Optional[Customer]:
        """Buscar cliente por DNI en un negocio"""
        query = self.db.query(Customer).filter(
            Customer.dni == dni,
            Customer.business_id == business_id,
            Customer.deleted_at.is_(None)
        )
        
        if exclude_id:
            query = query.filter(Customer.id != exclude_id)
        
        return query.first()
    
    def find_all(
        self,
        business_id: int,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Customer]:
        """Obtener todos los clientes de un negocio"""
        query = self.db.query(Customer).filter(
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
    
    def create(self, customer_data: dict) -> Customer:
        """Crear nuevo cliente"""
        customer = Customer(**customer_data)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def update(self, customer: Customer, update_data: dict) -> Customer:
        """Actualizar cliente existente"""
        for field, value in update_data.items():
            setattr(customer, field, value)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def soft_delete(self, customer: Customer) -> None:
        """Eliminar cliente (soft delete)"""
        customer.deleted_at = datetime.now()
        self.db.commit()

