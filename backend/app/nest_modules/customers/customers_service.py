"""
Servicio de clientes usando PyNest - Solo lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from .customers_repository import CustomerRepository
from ...models.customer import Customer
from ...schemas.customer import CustomerCreate, CustomerUpdate


@Injectable
class CustomersService:
    """Servicio para lógica de negocio de clientes"""
    
    def __init__(self):
        pass
    
    def create_customer(
        self,
        customer_data: CustomerCreate,
        business_id: int,
        db: Session
    ) -> Customer:
        """Crear nuevo cliente con validaciones"""
        customer_repo = CustomerRepository(db)
        
        # Validar DNI duplicado si se proporciona
        if customer_data.dni:
            existing = customer_repo.find_by_dni(customer_data.dni, business_id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un cliente con este DNI en tu negocio"
                )
        
        # Crear cliente
        customer_dict = {
            'business_id': business_id,
            'nombre': customer_data.nombre,
            'apellido': customer_data.apellido,
            'dni': customer_data.dni,
            'telefono': customer_data.telefono,
            'correo': customer_data.correo,
        }
        return customer_repo.create(customer_dict)
    
    def get_customers(
        self,
        business_id: int,
        skip: int,
        limit: int,
        search: Optional[str],
        db: Session
    ) -> List[Customer]:
        """Obtener lista de clientes"""
        customer_repo = CustomerRepository(db)
        return customer_repo.find_all(business_id, skip, limit, search)
    
    def get_customer_by_id(
        self,
        customer_id: int,
        business_id: int,
        db: Session
    ) -> Customer:
        """Obtener cliente por ID con validación"""
        customer_repo = CustomerRepository(db)
        customer = customer_repo.find_by_id(customer_id, business_id)
        
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
        """Actualizar cliente con validaciones"""
        customer_repo = CustomerRepository(db)
        
        # Validar que el cliente existe
        customer = customer_repo.find_by_id(customer_id, business_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Verificar DNI duplicado si se está actualizando
        if customer_update.dni and customer_update.dni != customer.dni:
            existing = customer_repo.find_by_dni(customer_update.dni, business_id, exclude_id=customer_id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otro cliente con este DNI en tu negocio"
                )
        
        # Actualizar
        update_data = customer_update.model_dump(exclude_unset=True)
        return customer_repo.update(customer, update_data)
    
    def delete_customer(self, customer_id: int, business_id: int, db: Session) -> None:
        """Eliminar cliente (soft delete) con validaciones"""
        customer_repo = CustomerRepository(db)
        
        # Validar que el cliente existe
        customer = customer_repo.find_by_id(customer_id, business_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Eliminar
        customer_repo.soft_delete(customer)

