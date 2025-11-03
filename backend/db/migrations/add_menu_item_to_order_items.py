"""
Migración para agregar menu_item_id a order_items
Permite que los items de orden puedan ser productos directos o items del menú
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import text
from app.database import engine

def migrate():
    print("Iniciando migración...")
    
    try:
        with engine.begin() as conn:
            # 1. Hacer product_id nullable
            print("1. Haciendo product_id nullable...")
            conn.execute(text("""
                ALTER TABLE order_items 
                ALTER COLUMN product_id DROP NOT NULL;
            """))
            
            # 2. Agregar menu_item_id como columna opcional
            print("2. Agregando menu_item_id...")
            conn.execute(text("""
                ALTER TABLE order_items 
                ADD COLUMN IF NOT EXISTS menu_item_id INTEGER;
            """))
            
            # 3. Agregar foreign key constraint
            print("3. Agregando foreign key constraint...")
            conn.execute(text("""
                ALTER TABLE order_items 
                ADD CONSTRAINT fk_order_items_menu_item 
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(id);
            """))
            
            # 4. Agregar source_type para tracking
            print("4. Agregando source_type...")
            conn.execute(text("""
                ALTER TABLE order_items 
                ADD COLUMN IF NOT EXISTS source_type VARCHAR(20) DEFAULT 'product';
            """))
            
            # 5. Actualizar registros existentes
            print("5. Actualizando registros existentes...")
            conn.execute(text("""
                UPDATE order_items 
                SET source_type = 'product' 
                WHERE source_type IS NULL;
            """))
            
        print("✅ Migración completada exitosamente!")
        print("\nColumnas agregadas:")
        print("  - menu_item_id (INTEGER, nullable, FK a menu_items)")
        print("  - source_type (VARCHAR(20), default 'product')")
        print("  - product_id ahora es nullable")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    migrate()

