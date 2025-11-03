"""
Script para agregar tabla order_payments y campo payment_status
Ejecutar: python migrate_add_order_payments.py
"""
from sqlalchemy import text
from app.database import engine

def migrate():
    print("🔧 Creando tabla order_payments y actualizando orders...")
    
    with engine.connect() as connection:
        try:
            # Crear tabla order_payments
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS order_payments (
                    id SERIAL PRIMARY KEY,
                    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                    payment_method_id INTEGER NOT NULL REFERENCES payment_methods(id),
                    amount DECIMAL(10,2) NOT NULL,
                    reference VARCHAR
                );
            """))
            connection.commit()
            print("✅ Tabla 'order_payments' creada")
            
            # Agregar campo payment_status a orders
            connection.execute(text("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS payment_status VARCHAR DEFAULT 'pending';
            """))
            connection.commit()
            print("✅ Campo 'payment_status' agregado a orders")
            
            # Crear índices
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_order_payments_order_id ON order_payments(order_id);
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_order_payments_payment_method_id ON order_payments(payment_method_id);
            """))
            connection.commit()
            print("✅ Índices creados")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 Ahora puedes ejecutar: python run.py\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Order Payments")
    print("="*50 + "\n")
    migrate()

