"""
Script para ejecutar la aplicación PyNest
"""
import uvicorn
import os
from app.core.database import init_db
from app.models.user import User, UserRole
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.utils.security import get_password_hash

def create_default_admin():
    """Crear usuario admin por defecto si no existe"""
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin = User(
                username="admin",
                email="admin@admin.admin",
                full_name="Administrador",
                hashed_password=get_password_hash("123456.Ab!"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("\n✅ Usuario administrador creado:")
            print("   Usuario: admin")
            print("   Email: admin@admin.admin")
            print("   Password: 123456.Ab!\n")
    except Exception as e:
        print(f"Error al crear admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando aplicación PyNest...")
    print("📦 Inicializando base de datos...")
    
    # Inicializar base de datos
    init_db()
    
    # Crear admin por defecto
    create_default_admin()
    
    print("✅ Base de datos inicializada")
    print("🌐 Servidor iniciando en http://localhost:8000")
    print("📖 Documentación disponible en http://localhost:8000/docs\n")
    
    # Ejecutar servidor
    uvicorn.run(
        "app_nest:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

