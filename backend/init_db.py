"""
Script para inicializar la base de datos con datos por defecto
"""
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

def init_database():
    """Crear tablas y datos iniciales"""
    print("🔧 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existe el usuario admin
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            print("\n👤 Creando usuario administrador por defecto...")
            
            # Crear usuario administrador
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
            db.refresh(admin)
            
            print("✅ Usuario administrador creado exitosamente")
            print("\n" + "="*50)
            print("📋 CREDENCIALES DE ACCESO")
            print("="*50)
            print(f"Usuario:    admin")
            print(f"Email:      admin@admin.admin")
            print(f"Password:   123456.Ab!")
            print(f"Rol:        Administrador")
            print("="*50 + "\n")
        else:
            print("ℹ️  El usuario administrador ya existe")
            print(f"   Usuario: {admin_user.username}")
            print(f"   Email:   {admin_user.email}")
            print(f"   Rol:     {admin_user.role.value}")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 INICIALIZACIÓN DE BASE DE DATOS")
    print("="*50 + "\n")
    
    init_database()
    
    print("\n✨ Proceso completado")
    print("💡 Ahora puedes ejecutar: python run.py\n")

