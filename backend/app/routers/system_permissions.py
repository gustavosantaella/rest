from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import get_db
from ..models.user import User
from ..models.role_permission import Permission
from ..schemas.role_permission import PermissionResponse
from ..utils.dependencies import get_current_active_admin
from ..utils.seed_permissions import SYSTEM_PERMISSIONS, get_permissions_by_module

router = APIRouter(prefix="/system-permissions", tags=["system-permissions"])


@router.get("/", response_model=List[PermissionResponse])
def get_all_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Obtener todos los permisos del sistema"""
    permissions = db.query(Permission).all()
    return permissions


@router.get("/by-module", response_model=Dict[str, List[PermissionResponse]])
def get_permissions_grouped_by_module(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Obtener permisos agrupados por módulo"""
    permissions = db.query(Permission).all()
    
    grouped = {}
    for perm in permissions:
        if perm.module not in grouped:
            grouped[perm.module] = []
        grouped[perm.module].append(perm)
    
    return grouped


@router.post("/seed", status_code=status.HTTP_200_OK)
def seed_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Crear permisos predefinidos del sistema (ejecutar una vez)"""
    created_count = 0
    existing_count = 0
    
    for perm_data in SYSTEM_PERMISSIONS:
        # Verificar si ya existe
        existing = db.query(Permission).filter(Permission.code == perm_data["code"]).first()
        
        if not existing:
            new_permission = Permission(**perm_data)
            db.add(new_permission)
            created_count += 1
        else:
            existing_count += 1
    
    db.commit()
    
    return {
        "message": "Permisos del sistema procesados",
        "created": created_count,
        "existing": existing_count,
        "total": len(SYSTEM_PERMISSIONS)
    }

