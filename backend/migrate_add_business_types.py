"""
Migración para agregar tabla business_types y columna business_type_id a business_configuration
"""

from sqlalchemy import create_engine, text
from app.database import Base, engine, SessionLocal
from app.models.business_type import BusinessType
from app.models.configuration import BusinessConfiguration
import sys

def migrate():
    """Ejecutar migración"""
    db = SessionLocal()
    try:
        print("🔄 Creando tabla business_types...")
        
        # Crear tabla business_types
        BusinessType.__table__.create(bind=engine, checkfirst=True)
        print("✅ Tabla business_types creada")
        
        # Agregar columna business_type_id a business_configuration si no existe
        print("🔄 Agregando columna business_type_id a business_configuration...")
        with engine.connect() as conn:
            # Verificar si la columna ya existe
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='business_configuration' 
                AND column_name='business_type_id'
            """))
            
            if result.fetchone() is None:
                # Agregar columna
                conn.execute(text("""
                    ALTER TABLE business_configuration 
                    ADD COLUMN business_type_id INTEGER 
                    REFERENCES business_types(id)
                """))
                conn.commit()
                print("✅ Columna business_type_id agregada")
            else:
                print("ℹ️  Columna business_type_id ya existe")
        
        # Insertar tipos de negocios por defecto
        print("🔄 Insertando tipos de negocios por defecto...")
        
        default_types = [
            {
                "name": "Restaurant",
                "slug": "restaurant",
                "description": "Restaurante con menú completo, mesas y servicio",
                "has_menu": True,
                "has_tables": True,
                "has_ingredients": True,
                "has_menu_statistics": True,
                "has_product_statistics": True
            },
            {
                "name": "Kiosko",
                "slug": "kiosko",
                "description": "Kiosko de comida rápida sin mesas",
                "has_menu": False,
                "has_tables": False,
                "has_ingredients": False,
                "has_menu_statistics": False,
                "has_product_statistics": True
            },
            {
                "name": "Vendedor Independiente",
                "slug": "vendedor-independiente",
                "description": "Vendedor independiente de productos",
                "has_menu": False,
                "has_tables": False,
                "has_ingredients": False,
                "has_menu_statistics": False,
                "has_product_statistics": True
            },
            {
                "name": "Venta de Productos",
                "slug": "venta-productos",
                "description": "Tienda de venta de productos",
                "has_menu": False,
                "has_tables": False,
                "has_ingredients": False,
                "has_menu_statistics": False,
                "has_product_statistics": True
            },
            {
                "name": "Cafetería",
                "slug": "cafeteria",
                "description": "Cafetería con menú limitado y mesas",
                "has_menu": True,
                "has_tables": True,
                "has_ingredients": True,
                "has_menu_statistics": True,
                "has_product_statistics": True
            },
            {
                "name": "Bar",
                "slug": "bar",
                "description": "Bar con bebidas y snacks",
                "has_menu": True,
                "has_tables": True,
                "has_ingredients": False,
                "has_menu_statistics": True,
                "has_product_statistics": True
            }
        ]
        
        for type_data in default_types:
            existing = db.query(BusinessType).filter(BusinessType.slug == type_data["slug"]).first()
            if not existing:
                business_type = BusinessType(**type_data)
                db.add(business_type)
                print(f"  ✅ Tipo '{type_data['name']}' creado")
            else:
                print(f"  ℹ️  Tipo '{type_data['name']}' ya existe")
        
        db.commit()
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error en la migración: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate()

