"""
Script para crear las tablas de cuentas por cobrar y cuentas por pagar
Ejecutar: python db/migrations/migrate_add_accounts_tables.py
"""
from sqlalchemy import text
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import engine

def migrate():
    print("🔧 Creando tablas de cuentas por cobrar y cuentas por pagar...")
    
    with engine.connect() as connection:
        try:
            # Crear tabla accounts_receivable
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS accounts_receivable (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL,
                    invoice_number VARCHAR,
                    description TEXT NOT NULL,
                    amount FLOAT NOT NULL,
                    amount_paid FLOAT DEFAULT 0.0,
                    amount_pending FLOAT NOT NULL,
                    issue_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    paid_date TIMESTAMP WITH TIME ZONE,
                    status VARCHAR NOT NULL DEFAULT 'pending',
                    notes TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    deleted_at TIMESTAMP WITH TIME ZONE
                );
            """))
            connection.commit()
            print("✅ Tabla 'accounts_receivable' creada")
            
            # Crear índices para accounts_receivable
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_receivable_business_id ON accounts_receivable(business_id);
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_receivable_customer_id ON accounts_receivable(customer_id);
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_receivable_invoice_number ON accounts_receivable(invoice_number);
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_receivable_status ON accounts_receivable(status);
            """))
            connection.commit()
            print("✅ Índices para 'accounts_receivable' creados")
            
            # Crear tabla account_receivable_payments
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS account_receivable_payments (
                    id SERIAL PRIMARY KEY,
                    account_id INTEGER NOT NULL REFERENCES accounts_receivable(id) ON DELETE CASCADE,
                    amount FLOAT NOT NULL,
                    payment_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    payment_method VARCHAR,
                    reference VARCHAR,
                    notes TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """))
            connection.commit()
            print("✅ Tabla 'account_receivable_payments' creada")
            
            # Crear tabla accounts_payable
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS accounts_payable (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    supplier_name VARCHAR NOT NULL,
                    supplier_phone VARCHAR,
                    supplier_email VARCHAR,
                    invoice_number VARCHAR,
                    description TEXT NOT NULL,
                    amount FLOAT NOT NULL,
                    amount_paid FLOAT DEFAULT 0.0,
                    amount_pending FLOAT NOT NULL,
                    issue_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    paid_date TIMESTAMP WITH TIME ZONE,
                    status VARCHAR NOT NULL DEFAULT 'pending',
                    notes TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE,
                    deleted_at TIMESTAMP WITH TIME ZONE
                );
            """))
            connection.commit()
            print("✅ Tabla 'accounts_payable' creada")
            
            # Crear índices para accounts_payable
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_payable_business_id ON accounts_payable(business_id);
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_payable_supplier_name ON accounts_payable(supplier_name);
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_payable_invoice_number ON accounts_payable(invoice_number);
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounts_payable_status ON accounts_payable(status);
            """))
            connection.commit()
            print("✅ Índices para 'accounts_payable' creados")
            
            # Crear tabla account_payable_payments
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS account_payable_payments (
                    id SERIAL PRIMARY KEY,
                    account_id INTEGER NOT NULL REFERENCES accounts_payable(id) ON DELETE CASCADE,
                    amount FLOAT NOT NULL,
                    payment_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    payment_method VARCHAR,
                    reference VARCHAR,
                    notes TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """))
            connection.commit()
            print("✅ Tabla 'account_payable_payments' creada")
            
            print("\n✨ Migración completada exitosamente!")
            print("💡 Las tablas de cuentas por cobrar y cuentas por pagar han sido creadas\n")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MIGRACIÓN: Crear Tablas de Cuentas")
    print("="*50 + "\n")
    migrate()

