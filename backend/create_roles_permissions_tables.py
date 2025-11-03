"""
Script de migración para crear tablas de roles y permisos
Ejecutar: python create_roles_permissions_tables.py
"""

from sqlalchemy import create_engine, text
from app.config import settings

def create_tables():
    """Crear tablas de roles y permisos"""
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # 1. Crear tabla de permisos (permissions)
            print("📋 Creando tabla 'permissions'...")
            create_permissions = text("""
                CREATE TABLE IF NOT EXISTS permissions (
                    id SERIAL PRIMARY KEY,
                    code VARCHAR UNIQUE NOT NULL,
                    name VARCHAR NOT NULL,
                    description TEXT,
                    module VARCHAR NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute(create_permissions)
            print("✅ Tabla 'permissions' creada")
            
            # 2. Crear tabla de roles (roles)
            print("📋 Creando tabla 'roles'...")
            create_roles = text("""
                CREATE TABLE IF NOT EXISTS roles (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    name VARCHAR NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    deleted_at TIMESTAMP WITH TIME ZONE
                )
            """)
            conn.execute(create_roles)
            print("✅ Tabla 'roles' creada")
            
            # 3. Crear tabla de relación role_permissions
            print("📋 Creando tabla 'role_permissions'...")
            create_role_permissions = text("""
                CREATE TABLE IF NOT EXISTS role_permissions (
                    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                    permission_id INTEGER NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (role_id, permission_id)
                )
            """)
            conn.execute(create_role_permissions)
            print("✅ Tabla 'role_permissions' creada")
            
            # 4. Crear tabla de relación user_roles
            print("📋 Creando tabla 'user_roles'...")
            create_user_roles = text("""
                CREATE TABLE IF NOT EXISTS user_roles (
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, role_id)
                )
            """)
            conn.execute(create_user_roles)
            print("✅ Tabla 'user_roles' creada")
            
            conn.commit()
            print("\n🎉 Todas las tablas creadas exitosamente!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()
    
    print("\n📝 Próximo paso: Ejecutar seed_system_permissions.py para crear los permisos predefinidos")

if __name__ == "__main__":
    print("🔄 Iniciando migración de tablas de roles y permisos...\n")
    create_tables()

