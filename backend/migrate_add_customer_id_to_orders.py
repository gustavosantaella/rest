"""
Migración para agregar columna customer_id a la tabla orders
"""
from sqlalchemy import create_engine, text
from app.database import engine
import sys

def migrate():
    """Ejecutar migración"""
    try:
        print("🔄 Agregando columna customer_id a orders...")
        
        with engine.connect() as conn:
            # Verificar si la columna ya existe
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='orders' 
                AND column_name='customer_id'
            """))
            
            if result.fetchone() is None:
                # Agregar columna customer_id
                conn.execute(text("""
                    ALTER TABLE orders 
                    ADD COLUMN customer_id INTEGER 
                    REFERENCES customers(id)
                """))
                conn.commit()
                print("✅ Columna customer_id agregada")
            else:
                print("ℹ️  Columna customer_id ya existe")
        
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en la migración: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()

