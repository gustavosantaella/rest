"""
Script para migrar la columna status de enum a VARCHAR
Ejecutar: python migrate_order_status_to_string.py
"""
import sys
import os

sys.path.append(os.path.dirname(__file__))

from sqlalchemy import text
from app.database import engine

def migrate_to_string():
    """
    Convierte la columna status de tipo enum a VARCHAR
    """
    with engine.connect() as conn:
        try:
            print("🔍 Verificando tipo actual de la columna status...")
            
            # Verificar el tipo actual
            result = conn.execute(text("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'orders' 
                AND column_name = 'status'
            """))
            current_type = result.scalar()
            print(f"   Tipo actual: {current_type}")
            
            if current_type == 'USER-DEFINED':
                print("\n📝 Convirtiendo columna 'status' de enum a VARCHAR...")
                
                # Convertir a VARCHAR manteniendo los valores
                conn.execute(text("""
                    ALTER TABLE orders 
                    ALTER COLUMN status TYPE VARCHAR 
                    USING status::VARCHAR
                """))
                conn.commit()
                print("✅ Columna convertida a VARCHAR")
                
                # Eliminar el enum ya que no se usa más
                print("📝 Eliminando tipo enum orderstatus...")
                conn.execute(text("DROP TYPE IF EXISTS orderstatus CASCADE"))
                conn.commit()
                print("✅ Tipo enum eliminado")
                
            elif current_type == 'character varying':
                print("✅ La columna ya es VARCHAR, no se necesita migración")
            else:
                print(f"⚠️  Tipo inesperado: {current_type}")
                
            # Verificar valores actuales
            print("\n📊 Valores actuales en la columna status:")
            result = conn.execute(text("""
                SELECT DISTINCT status 
                FROM orders 
                ORDER BY status
            """))
            
            for row in result:
                print(f"   - {row[0]}")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    print("=" * 60)
    print("Migración: OrderStatus de enum a VARCHAR")
    print("=" * 60)
    migrate_to_string()
    print("\n✅ Migración completada!")

