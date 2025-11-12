"""
Servicio de mesas usando PyNest
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from ...models.table import Table
from ...schemas.table import TableCreate, TableUpdate


@Injectable
class TablesService:
    """Servicio para manejo de mesas"""
    
    def __init__(self):
        pass
    
    def create_table(self, table_data: TableCreate, business_id: int, db: Session) -> Table:
        """Crear nueva mesa"""
        # Verificar número de mesa duplicado en el negocio
        existing = db.query(Table).filter(
            Table.number == table_data.number,
            Table.business_id == business_id,
            Table.deleted_at.is_(None)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de mesa ya existe en tu negocio"
            )
        
        table_dict = table_data.model_dump()
        table_dict['business_id'] = business_id
        new_table = Table(**table_dict)
        db.add(new_table)
        db.commit()
        db.refresh(new_table)
        return new_table
    
    def get_tables(self, business_id: int, skip: int, limit: int, db: Session) -> List[Table]:
        """Obtener lista de mesas del negocio"""
        return db.query(Table).filter(
            Table.business_id == business_id,
            Table.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def get_table_by_id(self, table_id: int, business_id: int, db: Session) -> Table:
        """Obtener mesa por ID"""
        table = db.query(Table).filter(
            Table.id == table_id,
            Table.business_id == business_id,
            Table.deleted_at.is_(None)
        ).first()
        
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
        """Actualizar mesa"""
        table = self.get_table_by_id(table_id, business_id, db)
        
        update_data = table_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(table, field, value)
        
        db.commit()
        db.refresh(table)
        return table
    
    def delete_table(self, table_id: int, business_id: int, db: Session) -> None:
        """Eliminar mesa (soft delete)"""
        table = self.get_table_by_id(table_id, business_id, db)
        table.deleted_at = datetime.now()
        db.commit()

