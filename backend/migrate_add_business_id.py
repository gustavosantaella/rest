"""
Migración: Agregar business_id a las tablas que no lo tienen
"""
from sqlalchemy import text
from app.core.database import SessionLocal
from app.models.user import User

def run_migration():
    """Ejecutar migración para agregar business_id"""
    
    db = SessionLocal()
    
    try:
        print("\n" + "="*70)
        print("🔄 MIGRACIÓN: Agregar business_id a tablas")
        print("="*70 + "\n")
        
        # Obtener un business_id por defecto de los usuarios existentes
        first_user = db.query(User).filter(User.business_id.isnot(None)).first()
        default_business_id = first_user.business_id if first_user else 1
        
        print(f"📊 Business ID por defecto para datos existentes: {default_business_id}\n")
        
        # Lista de migraciones
        tables_to_migrate = [
            {
                "name": "tables",
                "sql": f"""
                    -- Verificar si ya existe
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='tables' AND column_name='business_id'
                        ) THEN
                            -- Agregar columna
                            ALTER TABLE tables ADD COLUMN business_id INTEGER;
                            
                            -- Asignar valor por defecto
                            UPDATE tables SET business_id = {default_business_id} WHERE business_id IS NULL;
                            
                            -- Crear foreign key
                            ALTER TABLE tables ADD CONSTRAINT fk_tables_business 
                                FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                            
                            -- Hacer NOT NULL
                            ALTER TABLE tables ALTER COLUMN business_id SET NOT NULL;
                            
                            -- Crear índice
                            CREATE INDEX idx_tables_business_id ON tables(business_id);
                            
                            RAISE NOTICE 'business_id agregado a tables';
                        ELSE
                            RAISE NOTICE 'business_id ya existe en tables';
                        END IF;
                    END $$;
                """
            },
            {
                "name": "products",
                "sql": f"""
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='products' AND column_name='business_id'
                        ) THEN
                            ALTER TABLE products ADD COLUMN business_id INTEGER;
                            UPDATE products SET business_id = {default_business_id} WHERE business_id IS NULL;
                            ALTER TABLE products ADD CONSTRAINT fk_products_business 
                                FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                            ALTER TABLE products ALTER COLUMN business_id SET NOT NULL;
                            CREATE INDEX idx_products_business_id ON products(business_id);
                            RAISE NOTICE 'business_id agregado a products';
                        ELSE
                            RAISE NOTICE 'business_id ya existe en products';
                        END IF;
                    END $$;
                """
            },
            {
                "name": "categories",
                "sql": f"""
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='categories' AND column_name='business_id'
                        ) THEN
                            ALTER TABLE categories ADD COLUMN business_id INTEGER;
                            UPDATE categories SET business_id = {default_business_id} WHERE business_id IS NULL;
                            ALTER TABLE categories ADD CONSTRAINT fk_categories_business 
                                FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                            ALTER TABLE categories ALTER COLUMN business_id SET NOT NULL;
                            CREATE INDEX idx_categories_business_id ON categories(business_id);
                            
                            -- Quitar unique constraint de name
                            ALTER TABLE categories DROP CONSTRAINT IF EXISTS categories_name_key;
                            
                            RAISE NOTICE 'business_id agregado a categories';
                        ELSE
                            RAISE NOTICE 'business_id ya existe en categories';
                        END IF;
                    END $$;
                """
            },
            {
                "name": "menu_items",
                "sql": f"""
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='menu_items' AND column_name='business_id'
                        ) THEN
                            ALTER TABLE menu_items ADD COLUMN business_id INTEGER;
                            UPDATE menu_items SET business_id = {default_business_id} WHERE business_id IS NULL;
                            ALTER TABLE menu_items ADD CONSTRAINT fk_menu_items_business 
                                FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                            ALTER TABLE menu_items ALTER COLUMN business_id SET NOT NULL;
                            CREATE INDEX idx_menu_items_business_id ON menu_items(business_id);
                            RAISE NOTICE 'business_id agregado a menu_items';
                        ELSE
                            RAISE NOTICE 'business_id ya existe en menu_items';
                        END IF;
                    END $$;
                """
            },
            {
                "name": "menu_categories",
                "sql": f"""
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='menu_categories' AND column_name='business_id'
                        ) THEN
                            ALTER TABLE menu_categories ADD COLUMN business_id INTEGER;
                            UPDATE menu_categories SET business_id = {default_business_id} WHERE business_id IS NULL;
                            ALTER TABLE menu_categories ADD CONSTRAINT fk_menu_categories_business 
                                FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                            ALTER TABLE menu_categories ALTER COLUMN business_id SET NOT NULL;
                            CREATE INDEX idx_menu_categories_business_id ON menu_categories(business_id);
                            
                            -- Quitar unique constraint de name
                            ALTER TABLE menu_categories DROP CONSTRAINT IF EXISTS menu_categories_name_key;
                            
                            RAISE NOTICE 'business_id agregado a menu_categories';
                        ELSE
                            RAISE NOTICE 'business_id ya existe en menu_categories';
                        END IF;
                    END $$;
                """
            },
            {
                "name": "orders",
                "sql": f"""
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='orders' AND column_name='business_id'
                        ) THEN
                            ALTER TABLE orders ADD COLUMN business_id INTEGER;
                            
                            -- Asignar business_id basado en el usuario
                            UPDATE orders o SET business_id = u.business_id 
                            FROM users u WHERE o.user_id = u.id AND o.business_id IS NULL;
                            
                            -- Para órdenes sin usuario, usar default
                            UPDATE orders SET business_id = {default_business_id} WHERE business_id IS NULL;
                            
                            ALTER TABLE orders ADD CONSTRAINT fk_orders_business 
                                FOREIGN KEY (business_id) REFERENCES business_configuration(id);
                            ALTER TABLE orders ALTER COLUMN business_id SET NOT NULL;
                            CREATE INDEX idx_orders_business_id ON orders(business_id);
                            RAISE NOTICE 'business_id agregado a orders';
                        ELSE
                            RAISE NOTICE 'business_id ya existe en orders';
                        END IF;
                    END $$;
                """
            },
        ]
        
        # Ejecutar migraciones
        for migration in tables_to_migrate:
            table_name = migration["name"]
            print(f"📋 Procesando tabla '{table_name}'...")
            
            try:
                db.execute(text(migration["sql"]))
                db.commit()
                print(f"  ✅ Tabla '{table_name}' procesada correctamente\n")
            except Exception as e:
                print(f"  ⚠️  Error en tabla '{table_name}': {e}\n")
                db.rollback()
        
        print("="*70)
        print("🎉 ¡Migración completada!")
        print("="*70)
        print(f"\n📊 Business ID asignado a datos existentes: {default_business_id}")
        print("\n✅ Ahora puedes iniciar el servidor:")
        print("   python run_nest.py\n")
        
    except Exception as e:
        print(f"\n❌ Error general durante la migración: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n⚠️  ADVERTENCIA: Esta operación modificará la base de datos")
    print("Asegúrate de tener un backup antes de continuar\n")
    
    response = input("¿Deseas continuar con la migración? (si/no): ")
    
    if response.lower() in ['si', 's', 'yes', 'y']:
        run_migration()
    else:
        print("\n❌ Migración cancelada por el usuario")

