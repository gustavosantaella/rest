"""
Script para cambiar tipo de show_in_catalog de INTEGER a BOOLEAN
Ejecutar: python migrate_fix_show_in_catalog_type.py
"""
from sqlalchemy import text
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import engine

def migrate():
    print("🔧 Cambiando tipo de show_in_catalog a BOOLEAN...")
    
    with engine.connect() as connection:
        try:
            # Paso 1: Quitar el DEFAULT
            connection.execute(text("""
                ALTER TABLE products 
                ALTER COLUMN show_in_catalog 
                DROP DEFAULT;
            """))
            connection.commit()
            print("✅ DEFAULT eliminado temporalmente")
            
            # Paso 2: Cambiar tipo de INTEGER a BOOLEAN
            connection.execute(text("""
                ALTER TABLE products 
                ALTER COLUMN show_in_catalog 
                TYPE BOOLEAN 
                USING CASE WHEN show_in_catalog = 0 THEN FALSE ELSE TRUE END;
            """))
            connection.commit()
            print("✅ Tipo cambiado a BOOLEAN")
            
            # Paso 3: Agregar DEFAULT de nuevo
            connection.execute(text("""
                ALTER TABLE products 
                ALTER COLUMN show_in_catalog 
                SET DEFAULT FALSE;
            """))
            connection.commit()
            print("✅ DEFAULT FALSE agregado")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 Ahora puedes ejecutar: python run.py\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Fix show_in_catalog Type")
    print("="*50 + "\n")
    migrate()

