"""
Servicio de mesas usando PyNest - Solo lógica de negocio
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from .tables_repository import TableRepository
from ...models.table import Table
from ...schemas.table import TableCreate, TableUpdate


@Injectable
class TablesService:
    """Servicio para lógica de negocio de mesas"""
    
    def __init__(self):
        pass
    
    def create_table(self, table_data: TableCreate, business_id: int, db: Session) -> Table:
        """Crear nueva mesa con validaciones"""
        table_repo = TableRepository(db)
        
        # Validar número de mesa duplicado en el negocio
        existing = table_repo.find_by_number(table_data.number, business_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de mesa ya existe en tu negocio"
            )
        
        # Crear mesa
        table_dict = table_data.model_dump()
        table_dict['business_id'] = business_id
        return table_repo.create(table_dict)
    
    def get_tables(self, business_id: int, skip: int, limit: int, db: Session) -> List[Table]:
        """Obtener lista de mesas del negocio"""
        table_repo = TableRepository(db)
        return table_repo.find_all(business_id, skip, limit)
    
    def get_table_by_id(self, table_id: int, business_id: int, db: Session) -> Table:
        """Obtener mesa por ID con validación"""
        table_repo = TableRepository(db)
        table = table_repo.find_by_id(table_id, business_id)
        
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mesa no encontrada"
            )
        
        return table
    
    def update_table(
        self,
        table_id: int,
        table_update: TableUpdate,
        business_id: int,
        db: Session
    ) -> Table:
        """Actualizar mesa con validaciones"""
        table_repo = TableRepository(db)
        
        # Validar que la mesa existe
        table = table_repo.find_by_id(table_id, business_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mesa no encontrada"
            )
        
        # Actualizar
        update_data = table_update.model_dump(exclude_unset=True)
        return table_repo.update(table, update_data)
    
    def delete_table(self, table_id: int, business_id: int, db: Session) -> None:
        """Eliminar mesa (soft delete) con validaciones"""
        table_repo = TableRepository(db)
        
        # Validar que la mesa existe
        table = table_repo.find_by_id(table_id, business_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mesa no encontrada"
            )
        
        # Eliminar
        table_repo.soft_delete(table)

