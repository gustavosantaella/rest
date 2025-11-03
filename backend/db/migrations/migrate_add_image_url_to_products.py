"""
Migración: Agregar campo image_url a la tabla products
"""
from sqlalchemy import create_engine, text
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as connection:
        # Agregar columna image_url a products
        print("Agregando columna image_url a products...")
        connection.execute(text("""
            ALTER TABLE products 
            ADD COLUMN IF NOT EXISTS image_url VARCHAR;
        """))
        connection.commit()
        
        print("✅ Migración completada: image_url agregado a products")

if __name__ == "__main__":
    migrate()

