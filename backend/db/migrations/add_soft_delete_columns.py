"""
Script de migración para agregar columnas deleted_at a las tablas
Ejecutar: python add_soft_delete_columns.py
"""

from sqlalchemy import create_engine, text
from app.config import settings

def add_soft_delete_columns():
    """Agregar columna deleted_at a todas las tablas que necesitan soft delete"""
    
    engine = create_engine(settings.DATABASE_URL)
    
    # Lista de tablas que necesitan la columna deleted_at
    tables = [
        'users',
        'products',
        'categories',
        'menu_items',
        'menu_categories',
        'tables',
        'payment_methods',
        'order_items',
        'orders'
    ]
    
    with engine.connect() as conn:
        for table in tables:
            try:
                # Verificar si la columna ya existe
                check_query = text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='{table}' AND column_name='deleted_at'
                """)
                result = conn.execute(check_query)
                
                if result.fetchone() is None:
                    # La columna no existe, agregarla
                    alter_query = text(f"""
                        ALTER TABLE {table} 
                        ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE
                    """)
                    conn.execute(alter_query)
                    conn.commit()
                    print(f"✅ Columna deleted_at agregada a la tabla '{table}'")
                else:
                    print(f"ℹ️  La columna deleted_at ya existe en la tabla '{table}'")
                    
            except Exception as e:
                print(f"❌ Error al procesar la tabla '{table}': {e}")
                conn.rollback()
    
    print("\n🎉 Migración completada!")
    print("\nAhora puedes reiniciar tu servidor backend.")

if __name__ == "__main__":
    print("🔄 Iniciando migración para agregar columnas deleted_at...\n")
    add_soft_delete_columns()

