"""
Controlador de clientes usando PyNest
"""

from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List, Optional
from .customers_service import CustomersService
from ...core.database import get_db
from ...models.user import User
from ...schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate
from ...utils.dependencies import get_current_user


@Controller("api/customers")
class CustomersController:
    """Controlador para rutas de clientes"""

    def __init__(self, customers_service: CustomersService):
        self.customers_service = customers_service

    @Get("/")
    def read_customers(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> List[CustomerResponse]:
        """Obtener lista de clientes del negocio actual"""
        return self.customers_service.get_customers(
            current_user.business_id, skip, limit, search, db
        )

    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_customer(
        self,
        customer_data: CustomerCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> CustomerResponse:
        """Crear un nuevo cliente"""
        return self.customers_service.create_customer(
            customer_data, current_user.business_id, db
        )

    @Get("/{customer_id}")
    def read_customer(
        self,
        customer_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> CustomerResponse:
        """Obtener un cliente por ID"""
        return self.customers_service.get_customer_by_id(
            customer_id, current_user.business_id, db
        )

    @Put("/{customer_id}")
    def update_customer(
        self,
        customer_id: int,
        customer_update: CustomerUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> CustomerResponse:
        """Actualizar un cliente existente"""
        return self.customers_service.update_customer(
            customer_id, customer_update, current_user.business_id, db
        )

    @Delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_customer(
        self,
        customer_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        """Eliminar un cliente (soft delete)"""
        self.customers_service.delete_customer(
            customer_id, current_user.business_id, db
        )
        return None
