"""
Script para agregar business_id a modelos que no lo tienen
IMPORTANTE: Ejecutar esto actualizará la base de datos
"""
from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models.user import User

def add_business_id_to_tables():
    """Agregar columna business_id a las tablas que no la tienen"""
    
    db = SessionLocal()
    
    try:
        print("🔄 Iniciando migración para agregar business_id...")
        
        # Obtener el primer business_id disponible (para datos existentes)
        first_user = db.query(User).filter(User.business_id.isnot(None)).first()
        default_business_id = first_user.business_id if first_user else 1
        
        migrations = [
            {
                "table": "tables",
                "check": "SELECT column_name FROM information_schema.columns WHERE table_name='tables' AND column_name='business_id'",
                "add": f"""
                    ALTER TABLE tables ADD COLUMN business_id INTEGER;
                    ALTER TABLE tables ADD CONSTRAINT fk_tables_business 
                        FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                    UPDATE tables SET business_id = {default_business_id} WHERE business_id IS NULL;
                    ALTER TABLE tables ALTER COLUMN business_id SET NOT NULL;
                    CREATE INDEX idx_tables_business_id ON tables(business_id);
                """
            },
            {
                "table": "products",
                "check": "SELECT column_name FROM information_schema.columns WHERE table_name='products' AND column_name='business_id'",
                "add": f"""
                    ALTER TABLE products ADD COLUMN business_id INTEGER;
                    ALTER TABLE products ADD CONSTRAINT fk_products_business 
                        FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                    UPDATE products SET business_id = {default_business_id} WHERE business_id IS NULL;
                    ALTER TABLE products ALTER COLUMN business_id SET NOT NULL;
                    CREATE INDEX idx_products_business_id ON products(business_id);
                """
            },
            {
                "table": "categories",
                "check": "SELECT column_name FROM information_schema.columns WHERE table_name='categories' AND column_name='business_id'",
                "add": f"""
                    ALTER TABLE categories ADD COLUMN business_id INTEGER;
                    ALTER TABLE categories ADD CONSTRAINT fk_categories_business 
                        FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                    UPDATE categories SET business_id = {default_business_id} WHERE business_id IS NULL;
                    ALTER TABLE categories ALTER COLUMN business_id SET NOT NULL;
                    CREATE INDEX idx_categories_business_id ON categories(business_id);
                """
            },
            {
                "table": "menu_items",
                "check": "SELECT column_name FROM information_schema.columns WHERE table_name='menu_items' AND column_name='business_id'",
                "add": f"""
                    ALTER TABLE menu_items ADD COLUMN business_id INTEGER;
                    ALTER TABLE menu_items ADD CONSTRAINT fk_menu_items_business 
                        FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                    UPDATE menu_items SET business_id = {default_business_id} WHERE business_id IS NULL;
                    ALTER TABLE menu_items ALTER COLUMN business_id SET NOT NULL;
                    CREATE INDEX idx_menu_items_business_id ON menu_items(business_id);
                """
            },
            {
                "table": "menu_categories",
                "check": "SELECT column_name FROM information_schema.columns WHERE table_name='menu_categories' AND column_name='business_id'",
                "add": f"""
                    ALTER TABLE menu_categories ADD COLUMN business_id INTEGER;
                    ALTER TABLE menu_categories ADD CONSTRAINT fk_menu_categories_business 
                        FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                    UPDATE menu_categories SET business_id = {default_business_id} WHERE business_id IS NULL;
                    ALTER TABLE menu_categories ALTER COLUMN business_id SET NOT NULL;
                    CREATE INDEX idx_menu_categories_business_id ON menu_categories(business_id);
                """
            },
            {
                "table": "orders",
                "check": "SELECT column_name FROM information_schema.columns WHERE table_name='orders' AND column_name='business_id'",
                "add": f"""
                    ALTER TABLE orders ADD COLUMN business_id INTEGER;
                    UPDATE orders o SET business_id = u.business_id 
                        FROM users u WHERE o.user_id = u.id;
                    ALTER TABLE orders ADD CONSTRAINT fk_orders_business 
                        FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                    ALTER TABLE orders ALTER COLUMN business_id SET NOT NULL;
                    CREATE INDEX idx_orders_business_id ON orders(business_id);
                """
            },
        ]
        
        for migration in migrations:
            table_name = migration["table"]
            print(f"\n📋 Verificando tabla '{table_name}'...")
            
            # Verificar si ya tiene la columna
            result = db.execute(text(migration["check"]))
            if result.fetchone():
                print(f"  ✅ La tabla '{table_name}' ya tiene business_id")
                continue
            
            print(f"  ➕ Agregando business_id a '{table_name}'...")
            
            # Ejecutar la migración
            for statement in migration["add"].strip().split(';'):
                if statement.strip():
                    db.execute(text(statement))
            
            db.commit()
            print(f"  ✅ business_id agregado a '{table_name}'")
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print(f"📊 Business ID por defecto usado: {default_business_id}")
        print("\n⚠️  IMPORTANTE: Actualiza tus modelos SQLAlchemy para incluir el campo business_id")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante la migración: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRACIÓN: Agregar business_id a tablas")
    print("=" * 60)
    print("\n⚠️  ADVERTENCIA: Esta operación modificará la base de datos")
    print("Asegúrate de tener un backup antes de continuar\n")
    
    response = input("¿Deseas continuar? (si/no): ")
    
    if response.lower() in ['si', 's', 'yes', 'y']:
        add_business_id_to_tables()
    else:
        print("\n❌ Migración cancelada")

