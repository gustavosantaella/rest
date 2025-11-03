"""
Script para agregar campos de cliente a la tabla orders
Ejecutar: python migrate_add_customer_fields.py
"""
from sqlalchemy import text
from app.database import engine

def migrate():
    print("🔧 Agregando campos de cliente a la tabla orders...")
    
    with engine.connect() as connection:
        try:
            # Agregar campos de cliente
            connection.execute(text("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS customer_name VARCHAR;
            """))
            connection.commit()
            print("✅ Campo 'customer_name' agregado")
            
            connection.execute(text("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS customer_email VARCHAR;
            """))
            connection.commit()
            print("✅ Campo 'customer_email' agregado")
            
            connection.execute(text("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS customer_phone VARCHAR;
            """))
            connection.commit()
            print("✅ Campo 'customer_phone' agregado")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 Ahora puedes ejecutar: python run.py\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Campos de Cliente en Orders")
    print("="*50 + "\n")
    migrate()

