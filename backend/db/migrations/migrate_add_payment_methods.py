"""
Script para agregar tabla payment_methods
Ejecutar: python migrate_add_payment_methods.py
"""
from sqlalchemy import text
from app.database import engine

def migrate():
    print("🔧 Creando tabla payment_methods...")
    
    with engine.connect() as connection:
        try:
            # Crear tabla payment_methods
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS payment_methods (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    type VARCHAR NOT NULL,
                    phone VARCHAR,
                    dni VARCHAR,
                    bank VARCHAR,
                    account_holder VARCHAR,
                    account_number VARCHAR,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE
                );
            """))
            connection.commit()
            print("✅ Tabla 'payment_methods' creada")
            
            # Crear índices
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_payment_methods_type ON payment_methods(type);
            """))
            connection.commit()
            print("✅ Índices creados")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 Ahora puedes ejecutar: python run.py\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Tabla Payment Methods")
    print("="*50 + "\n")
    migrate()

