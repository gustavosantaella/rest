"""
Script para agregar campo show_in_catalog a products
Ejecutar: python migrate_add_show_in_catalog.py
"""
from sqlalchemy import text
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import engine

def migrate():
    print("🔧 Agregando campo show_in_catalog a productos...")
    
    with engine.connect() as connection:
        try:
            # Agregar campo show_in_catalog
            connection.execute(text("""
                ALTER TABLE products 
                ADD COLUMN IF NOT EXISTS show_in_catalog INTEGER DEFAULT 0;
            """))
            connection.commit()
            print("✅ Campo 'show_in_catalog' agregado (por defecto: 0 = No mostrar)")
            
            # Crear índice para búsquedas más rápidas
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_products_show_in_catalog ON products(show_in_catalog);
            """))
            connection.commit()
            print("✅ Índice creado")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 Ahora puedes ejecutar: python run.py\n")
            print("ℹ️  Por defecto todos los productos están ocultos del catálogo.")
            print("   Edita cada producto y marca 'Mostrar en catálogo' para que aparezcan en órdenes.\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Show in Catalog Field")
    print("="*50 + "\n")
    migrate()

