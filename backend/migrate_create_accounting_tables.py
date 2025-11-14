"""
Migración para crear tablas del módulo contable
"""
from sqlalchemy import create_engine, text
from app.database import engine
import sys

def migrate():
    """Ejecutar migración"""
    try:
        print("🔄 Creando tablas del módulo contable...")
        
        with engine.connect() as conn:
            # Crear tabla chart_of_accounts
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS chart_of_accounts (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    code VARCHAR NOT NULL,
                    name VARCHAR NOT NULL,
                    description TEXT,
                    account_type VARCHAR NOT NULL,
                    nature VARCHAR NOT NULL,
                    parent_id INTEGER REFERENCES chart_of_accounts(id),
                    level INTEGER DEFAULT 1,
                    allows_manual_entries BOOLEAN DEFAULT TRUE,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_system BOOLEAN DEFAULT FALSE,
                    initial_balance NUMERIC(15, 2) DEFAULT 0,
                    initial_balance_date TIMESTAMP WITH TIME ZONE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE,
                    deleted_at TIMESTAMP WITH TIME ZONE,
                    UNIQUE(business_id, code)
                )
            """))
            
            # Crear índices para chart_of_accounts
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_chart_of_accounts_business_id ON chart_of_accounts(business_id);
                CREATE INDEX IF NOT EXISTS idx_chart_of_accounts_code ON chart_of_accounts(code);
                CREATE INDEX IF NOT EXISTS idx_chart_of_accounts_parent_id ON chart_of_accounts(parent_id);
            """))
            
            # Crear tabla accounting_periods
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS accounting_periods (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    name VARCHAR NOT NULL,
                    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    is_closed BOOLEAN DEFAULT FALSE,
                    closed_at TIMESTAMP WITH TIME ZONE,
                    closed_by INTEGER REFERENCES users(id),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE
                )
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_accounting_periods_business_id ON accounting_periods(business_id);
            """))
            
            # Crear tabla cost_centers
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS cost_centers (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    code VARCHAR NOT NULL,
                    name VARCHAR NOT NULL,
                    description TEXT,
                    parent_id INTEGER REFERENCES cost_centers(id),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE,
                    deleted_at TIMESTAMP WITH TIME ZONE,
                    UNIQUE(business_id, code)
                )
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_cost_centers_business_id ON cost_centers(business_id);
                CREATE INDEX IF NOT EXISTS idx_cost_centers_code ON cost_centers(code);
            """))
            
            # Crear tabla journal_entries
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    entry_number VARCHAR UNIQUE NOT NULL,
                    entry_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    reference VARCHAR,
                    description TEXT NOT NULL,
                    status VARCHAR NOT NULL DEFAULT 'draft',
                    posted_at TIMESTAMP WITH TIME ZONE,
                    posted_by INTEGER REFERENCES users(id),
                    reversed_entry_id INTEGER REFERENCES journal_entries(id),
                    is_reversal BOOLEAN DEFAULT FALSE,
                    period_id INTEGER REFERENCES accounting_periods(id),
                    created_by INTEGER NOT NULL REFERENCES users(id),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE,
                    deleted_at TIMESTAMP WITH TIME ZONE
                )
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_journal_entries_business_id ON journal_entries(business_id);
                CREATE INDEX IF NOT EXISTS idx_journal_entries_entry_number ON journal_entries(entry_number);
                CREATE INDEX IF NOT EXISTS idx_journal_entries_entry_date ON journal_entries(entry_date);
                CREATE INDEX IF NOT EXISTS idx_journal_entries_period_id ON journal_entries(period_id);
            """))
            
            # Crear tabla journal_entry_lines
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS journal_entry_lines (
                    id SERIAL PRIMARY KEY,
                    entry_id INTEGER NOT NULL REFERENCES journal_entries(id) ON DELETE CASCADE,
                    account_id INTEGER NOT NULL REFERENCES chart_of_accounts(id),
                    debit NUMERIC(15, 2) DEFAULT 0,
                    credit NUMERIC(15, 2) DEFAULT 0,
                    description TEXT,
                    reference VARCHAR,
                    cost_center_id INTEGER REFERENCES cost_centers(id),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_journal_entry_lines_entry_id ON journal_entry_lines(entry_id);
                CREATE INDEX IF NOT EXISTS idx_journal_entry_lines_account_id ON journal_entry_lines(account_id);
            """))
            
            # Crear tabla general_ledger
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS general_ledger (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER NOT NULL REFERENCES business_configuration(id) ON DELETE CASCADE,
                    account_id INTEGER NOT NULL REFERENCES chart_of_accounts(id),
                    period_id INTEGER REFERENCES accounting_periods(id),
                    entry_date TIMESTAMP WITH TIME ZONE NOT NULL,
                    entry_id INTEGER NOT NULL REFERENCES journal_entries(id),
                    entry_line_id INTEGER NOT NULL REFERENCES journal_entry_lines(id),
                    debit NUMERIC(15, 2) DEFAULT 0,
                    credit NUMERIC(15, 2) DEFAULT 0,
                    balance_debit NUMERIC(15, 2) DEFAULT 0,
                    balance_credit NUMERIC(15, 2) DEFAULT 0,
                    description TEXT,
                    reference VARCHAR,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_general_ledger_business_id ON general_ledger(business_id);
                CREATE INDEX IF NOT EXISTS idx_general_ledger_account_id ON general_ledger(account_id);
                CREATE INDEX IF NOT EXISTS idx_general_ledger_entry_date ON general_ledger(entry_date);
                CREATE INDEX IF NOT EXISTS idx_general_ledger_period_id ON general_ledger(period_id);
            """))
            
            conn.commit()
            print("✅ Tablas del módulo contable creadas exitosamente")
        
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en la migración: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    migrate()

