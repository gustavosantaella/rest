"""
Script para crear la tabla customers
Ejecutar: python db/migrations/migrate_add_customers_table.py
"""
from sqlalchemy import text
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import engine

def migrate():
    print("🔧 Creando tabla customers...")
    
    with engine.connect() as connection:
        try:
            # Crear tabla customers
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    nombre VARCHAR NOT NULL,
                    apellido VARCHAR,
                    dni VARCHAR,
                    telefono VARCHAR,
                    correo VARCHAR,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    deleted_at TIMESTAMP WITH TIME ZONE
                );
            """))
            connection.commit()
            print("✅ Tabla 'customers' creada")
            
            # Crear índices
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_customers_business_id ON customers(business_id);
            """))
            connection.commit()
            print("✅ Índice 'idx_customers_business_id' creado")
            
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_customers_nombre ON customers(nombre);
            """))
            connection.commit()
            print("✅ Índice 'idx_customers_nombre' creado")
            
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_customers_dni ON customers(dni);
            """))
            connection.commit()
            print("✅ Índice 'idx_customers_dni' creado")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 La tabla customers ha sido creada con todos sus campos e índices\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Crear Tabla Customers")
    print("="*50 + "\n")
    migrate()

