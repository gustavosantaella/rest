from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.table import Table
from ..models.user import User
from ..schemas.table import TableCreate, TableUpdate, TableResponse
from ..utils.dependencies import get_current_user, get_current_active_manager

router = APIRouter(prefix="/tables", tags=["tables"])


@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(
    table: TableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    db_table = db.query(Table).filter(
        Table.number == table.number,
        Table.deleted_at.is_(None)  # Solo mesas no eliminadas
    ).first()
    if db_table:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de mesa ya existe",
        )

    new_table = Table(**table.model_dump())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table


@router.get("/", response_model=List[TableResponse])
def read_tables(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tables = db.query(Table).filter(
        Table.deleted_at.is_(None)  # Solo mesas no eliminadas
    ).offset(skip).limit(limit).all()
    return tables


@router.get("/{table_id}", response_model=TableResponse)
def read_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    table = db.query(Table).filter(
        Table.id == table_id,
        Table.deleted_at.is_(None)  # Solo mesas no eliminadas
    ).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada"
        )
    return table


@router.put("/{table_id}", response_model=TableResponse)
def update_table(
    table_id: int,
    table_update: TableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    table = db.query(Table).filter(
        Table.id == table_id,
        Table.deleted_at.is_(None)  # Solo mesas no eliminadas
    ).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada"
        )

    update_data = table_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(table, field, value)

    db.commit()
    db.refresh(table)
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_manager),
):
    from datetime import datetime
    
    table = db.query(Table).filter(
        Table.id == table_id,
        Table.deleted_at.is_(None)  # Solo mesas no eliminadas
    ).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada"
        )

    # Soft delete: marcar como eliminado con timestamp
    table.deleted_at = datetime.now()
    db.commit()
    return None
