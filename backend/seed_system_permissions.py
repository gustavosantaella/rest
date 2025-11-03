"""
Script para crear los permisos predefinidos del sistema
Ejecutar: python seed_system_permissions.py
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.role_permission import Permission
from app.utils.seed_permissions import SYSTEM_PERMISSIONS

def seed_permissions():
    """Insertar permisos predefinidos en la base de datos"""
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        created_count = 0
        existing_count = 0
        
        print("📋 Insertando permisos del sistema...\n")
        
        for perm_data in SYSTEM_PERMISSIONS:
            # Verificar si ya existe
            existing = db.query(Permission).filter(Permission.code == perm_data["code"]).first()
            
            if not existing:
                new_permission = Permission(
                    code=perm_data["code"],
                    name=perm_data["name"],
                    description=perm_data.get("description"),
                    module=perm_data["module"]
                )
                db.add(new_permission)
                created_count += 1
                print(f"✅ Creado: {perm_data['code']} - {perm_data['name']}")
            else:
                existing_count += 1
                print(f"ℹ️  Ya existe: {perm_data['code']}")
        
        db.commit()
        
        print(f"\n🎉 Proceso completado!")
        print(f"   ✅ Permisos creados: {created_count}")
        print(f"   ℹ️  Permisos existentes: {existing_count}")
        print(f"   📊 Total de permisos: {len(SYSTEM_PERMISSIONS)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔄 Iniciando creación de permisos del sistema...\n")
    seed_permissions()

