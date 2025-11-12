"""
Repositorio de mesas - Operaciones de base de datos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...models.table import Table


class TableRepository:
    """Repositorio para operaciones de BD de mesas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_number(self, number: str, business_id: int) -> Optional[Table]:
        """Buscar mesa por número en un negocio"""
        return self.db.query(Table).filter(
            Table.number == number,
            Table.business_id == business_id,
            Table.deleted_at.is_(None)
        ).first()
    
    def find_by_id(self, table_id: int, business_id: int) -> Optional[Table]:
        """Buscar mesa por ID en un negocio"""
        return self.db.query(Table).filter(
            Table.id == table_id,
            Table.business_id == business_id,
            Table.deleted_at.is_(None)
        ).first()
    
    def find_all(self, business_id: int, skip: int = 0, limit: int = 100) -> List[Table]:
        """Obtener todas las mesas de un negocio"""
        return self.db.query(Table).filter(
            Table.business_id == business_id,
            Table.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def create(self, table_data: dict) -> Table:
        """Crear nueva mesa"""
        table = Table(**table_data)
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table
    
    def update(self, table: Table, update_data: dict) -> Table:
        """Actualizar mesa existente"""
        for field, value in update_data.items():
            setattr(table, field, value)
        self.db.commit()
        self.db.refresh(table)
        return table
    
    def soft_delete(self, table: Table) -> None:
        """Eliminar mesa (soft delete)"""
        table.deleted_at = datetime.now()
        self.db.commit()

