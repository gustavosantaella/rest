"""
Script de migración para crear la tabla user_permissions
Ejecutar: python create_permissions_table.py
"""

from sqlalchemy import create_engine, text
from app.config import settings

def create_permissions_table():
    """Crear tabla user_permissions para el sistema de permisos"""
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Verificar si la tabla ya existe
            check_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name='user_permissions'
            """)
            result = conn.execute(check_query)
            
            if result.fetchone() is None:
                # Crear la tabla
                create_query = text("""
                    CREATE TABLE user_permissions (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        can_access_dashboard BOOLEAN DEFAULT true,
                        can_access_inventory BOOLEAN DEFAULT false,
                        can_access_products BOOLEAN DEFAULT false,
                        can_access_menu BOOLEAN DEFAULT false,
                        can_access_tables BOOLEAN DEFAULT false,
                        can_access_orders BOOLEAN DEFAULT false,
                        can_access_users BOOLEAN DEFAULT false,
                        can_access_configuration BOOLEAN DEFAULT false,
                        can_access_reports BOOLEAN DEFAULT false,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE,
                        UNIQUE(user_id)
                    )
                """)
                conn.execute(create_query)
                conn.commit()
                print("✅ Tabla 'user_permissions' creada exitosamente")
            else:
                print("ℹ️  La tabla 'user_permissions' ya existe")
                
        except Exception as e:
            print(f"❌ Error al crear la tabla: {e}")
            conn.rollback()
    
    print("\n🎉 Migración completada!")
    print("\nAhora puedes reiniciar tu servidor backend.")

if __name__ == "__main__":
    print("🔄 Iniciando migración para crear tabla user_permissions...\n")
    create_permissions_table()

