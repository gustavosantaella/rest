"""
Controlador de mesas usando PyNest
"""
from nest.core import Controller, Get, Post, Put, Delete, Depends
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from .tables_service import TablesService
from ...core.database import get_db
from ...models.user import User
from ...schemas.table import TableCreate, TableUpdate, TableResponse
from ...utils.dependencies import get_current_user, get_current_active_manager


@Controller("api/tables")
class TablesController:
    """Controlador para rutas de mesas"""
    
    def __init__(self, tables_service: TablesService):
        self.tables_service = tables_service
    
    @Post("/", status_code=status.HTTP_201_CREATED)
    def create_table(
        self,
        table: TableCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ) -> TableResponse:
        """Crear nueva mesa"""
        return self.tables_service.create_table(table, current_user.business_id, db)
    
    @Get("/")
    def read_tables(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> List[TableResponse]:
        """Obtener lista de mesas"""
        return self.tables_service.get_tables(current_user.business_id, skip, limit, db)
    
    @Get("/{table_id}")
    def read_table(
        self,
        table_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> TableResponse:
        """Obtener mesa por ID"""
        return self.tables_service.get_table_by_id(table_id, current_user.business_id, db)
    
    @Put("/{table_id}")
    def update_table(
        self,
        table_id: int,
        table_update: TableUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> TableResponse:
        """Actualizar mesa"""
        return self.tables_service.update_table(table_id, table_update, current_user.business_id, db)
    
    @Delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_table(
        self,
        table_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_manager)
    ):
        """Eliminar mesa (soft delete)"""
        self.tables_service.delete_table(table_id, current_user.business_id, db)
        return None

