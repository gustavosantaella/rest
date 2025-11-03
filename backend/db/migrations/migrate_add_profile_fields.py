"""
Script para agregar campos de perfil a la tabla users
Ejecutar: python migrate_add_profile_fields.py
"""
from sqlalchemy import text
from app.database import engine

def migrate():
    print("🔧 Agregando campos de perfil a la tabla users...")
    
    with engine.connect() as connection:
        try:
            # Agregar columna dni
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS dni VARCHAR UNIQUE;
            """))
            connection.commit()
            print("✅ Columna 'dni' agregada")
            
            # Agregar columna country
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS country VARCHAR;
            """))
            connection.commit()
            print("✅ Columna 'country' agregada")
            
            # Crear índice para dni
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_dni ON users(dni);
            """))
            connection.commit()
            print("✅ Índice para 'dni' creado")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 Ahora puedes ejecutar: python run.py\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Agregar Campos de Perfil")
    print("="*50 + "\n")
    migrate()

