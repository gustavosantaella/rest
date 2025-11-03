"""
Migración: Agregar campo slug a business_configuration
"""
from sqlalchemy import create_engine, text
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import settings
import re

def generate_slug(business_name: str) -> str:
    """Genera un slug único a partir del nombre del negocio"""
    slug = business_name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    return slug or 'mi-negocio'

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as connection:
        # Agregar columna slug
        print("Agregando columna slug a business_configuration...")
        connection.execute(text("""
            ALTER TABLE business_configuration 
            ADD COLUMN IF NOT EXISTS slug VARCHAR UNIQUE;
        """))
        connection.commit()
        
        # Obtener negocios existentes sin slug
        result = connection.execute(text("""
            SELECT id, business_name 
            FROM business_configuration 
            WHERE slug IS NULL;
        """))
        
        businesses = result.fetchall()
        
        # Generar slugs para negocios existentes
        for business in businesses:
            business_id, business_name = business
            slug = generate_slug(business_name)
            
            # Asegurar que el slug es único
            counter = 1
            original_slug = slug
            while True:
                check = connection.execute(text("""
                    SELECT id FROM business_configuration WHERE slug = :slug
                """), {"slug": slug})
                if check.fetchone() is None:
                    break
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Actualizar el slug
            connection.execute(text("""
                UPDATE business_configuration 
                SET slug = :slug 
                WHERE id = :id
            """), {"slug": slug, "id": business_id})
            print(f"  ✓ Negocio '{business_name}' → slug: '{slug}'")
        
        connection.commit()
        
        # Crear índice si no existe
        print("Creando índice en slug...")
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_business_slug 
            ON business_configuration(slug);
        """))
        connection.commit()
        
        print("✅ Migración completada: slug agregado a business_configuration")

if __name__ == "__main__":
    migrate()

