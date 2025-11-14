"""
Migración para agregar columna order_id a la tabla accounts_receivable
"""
from sqlalchemy import create_engine, text
from app.database import engine
import sys

def migrate():
    """Ejecutar migración"""
    try:
        print("🔄 Agregando columna order_id a accounts_receivable...")
        
        with engine.connect() as conn:
            # Verificar si la columna ya existe
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='accounts_receivable' 
                AND column_name='order_id'
            """))
            
            if result.fetchone() is None:
                # Agregar columna order_id
                conn.execute(text("""
                    ALTER TABLE accounts_receivable 
                    ADD COLUMN order_id INTEGER 
                    REFERENCES orders(id) ON DELETE SET NULL
                """))
                conn.commit()
                print("✅ Columna order_id agregada")
            else:
                print("ℹ️  Columna order_id ya existe")
        
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en la migración: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()

