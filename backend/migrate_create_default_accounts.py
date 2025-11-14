"""
Migración para crear cuentas contables por defecto
"""
from sqlalchemy import create_engine, text
from app.database import engine, SessionLocal
from app.models.accounting import ChartOfAccounts, AccountType, AccountNature
import sys

def migrate():
    """Crear cuentas contables por defecto para cada negocio"""
    db = SessionLocal()
    try:
        print("🔄 Creando cuentas contables por defecto...")
        
        # Obtener todos los negocios
        with engine.connect() as conn:
            businesses = conn.execute(text("""
                SELECT id FROM business_configuration
            """)).fetchall()
            
            if not businesses:
                print("ℹ️  No hay negocios configurados. Las cuentas se crearán cuando se configure el primer negocio.")
                return
            
            for (business_id,) in businesses:
                print(f"\n📊 Creando cuentas para negocio ID: {business_id}")
                
                # Verificar si ya tiene cuentas
                existing = db.query(ChartOfAccounts).filter(
                    ChartOfAccounts.business_id == business_id
                ).first()
                
                if existing:
                    print(f"  ℹ️  El negocio {business_id} ya tiene cuentas contables. Omitiendo...")
                    continue
                
                # Cuentas por defecto
                default_accounts = [
                    # ACTIVOS
                    {
                        "code": "1.01.01",
                        "name": "Efectivo y Equivalentes",
                        "description": "Efectivo en caja y bancos",
                        "account_type": AccountType.ASSET,
                        "nature": AccountNature.DEBIT,
                        "level": 2,
                        "is_system": True
                    },
                    {
                        "code": "1.01.01.001",
                        "name": "Caja",
                        "description": "Efectivo en caja",
                        "account_type": AccountType.ASSET,
                        "nature": AccountNature.DEBIT,
                        "level": 3,
                        "is_system": True
                    },
                    {
                        "code": "1.01.01.002",
                        "name": "Bancos",
                        "description": "Cuentas bancarias",
                        "account_type": AccountType.ASSET,
                        "nature": AccountNature.DEBIT,
                        "level": 3,
                        "is_system": True
                    },
                    {
                        "code": "1.01.02",
                        "name": "Inventario",
                        "description": "Inventario de productos",
                        "account_type": AccountType.ASSET,
                        "nature": AccountNature.DEBIT,
                        "level": 2,
                        "is_system": True
                    },
                    {
                        "code": "1.01.03",
                        "name": "Cuentas por Cobrar",
                        "description": "Cuentas por cobrar a clientes",
                        "account_type": AccountType.ASSET,
                        "nature": AccountNature.DEBIT,
                        "level": 2,
                        "is_system": True
                    },
                    
                    # PASIVOS
                    {
                        "code": "2.01.01",
                        "name": "Cuentas por Pagar",
                        "description": "Cuentas por pagar a proveedores",
                        "account_type": AccountType.LIABILITY,
                        "nature": AccountNature.CREDIT,
                        "level": 2,
                        "is_system": True
                    },
                    
                    # PATRIMONIO
                    {
                        "code": "3.01.01",
                        "name": "Capital",
                        "description": "Capital del negocio",
                        "account_type": AccountType.EQUITY,
                        "nature": AccountNature.CREDIT,
                        "level": 2,
                        "is_system": True
                    },
                    {
                        "code": "3.01.02",
                        "name": "Utilidades Acumuladas",
                        "description": "Utilidades retenidas",
                        "account_type": AccountType.EQUITY,
                        "nature": AccountNature.CREDIT,
                        "level": 2,
                        "is_system": True
                    },
                    
                    # INGRESOS
                    {
                        "code": "4.01.01",
                        "name": "Ingresos por Ventas",
                        "description": "Ingresos por venta de productos y servicios",
                        "account_type": AccountType.REVENUE,
                        "nature": AccountNature.CREDIT,
                        "level": 2,
                        "is_system": True
                    },
                    
                    # COSTO DE VENTAS
                    {
                        "code": "5.01.01",
                        "name": "Costo de Ventas",
                        "description": "Costo de los productos vendidos",
                        "account_type": AccountType.COST_OF_SALES,
                        "nature": AccountNature.DEBIT,
                        "level": 2,
                        "is_system": True
                    },
                    
                    # GASTOS
                    {
                        "code": "6.01.01",
                        "name": "Gastos Operativos",
                        "description": "Gastos generales de operación",
                        "account_type": AccountType.EXPENSE,
                        "nature": AccountNature.DEBIT,
                        "level": 2,
                        "is_system": True
                    },
                    {
                        "code": "6.01.01.001",
                        "name": "Gastos de Personal",
                        "description": "Salarios y beneficios",
                        "account_type": AccountType.EXPENSE,
                        "nature": AccountNature.DEBIT,
                        "level": 3,
                        "is_system": True
                    },
                    {
                        "code": "6.01.01.002",
                        "name": "Gastos de Alquiler",
                        "description": "Alquiler de local",
                        "account_type": AccountType.EXPENSE,
                        "nature": AccountNature.DEBIT,
                        "level": 3,
                        "is_system": True
                    },
                    {
                        "code": "6.01.01.003",
                        "name": "Gastos de Servicios",
                        "description": "Servicios públicos (luz, agua, internet)",
                        "account_type": AccountType.EXPENSE,
                        "nature": AccountNature.DEBIT,
                        "level": 3,
                        "is_system": True
                    }
                ]
                
                # Crear cuentas usando SQL directo
                created_count = 0
                with engine.connect() as conn:
                    for acc_data in default_accounts:
                        # Verificar si ya existe
                        existing = conn.execute(text("""
                            SELECT id FROM chart_of_accounts 
                            WHERE business_id = :business_id AND code = :code
                        """), {"business_id": business_id, "code": acc_data["code"]}).fetchone()
                        
                        if not existing:
                            # Convertir Enum a string
                            account_type = acc_data['account_type'].value if hasattr(acc_data['account_type'], 'value') else str(acc_data['account_type'])
                            nature = acc_data['nature'].value if hasattr(acc_data['nature'], 'value') else str(acc_data['nature'])
                            
                            conn.execute(text("""
                                INSERT INTO chart_of_accounts 
                                (business_id, code, name, description, account_type, nature, level, 
                                 allows_manual_entries, is_active, is_system, initial_balance)
                                VALUES 
                                (:business_id, :code, :name, :description, :account_type, :nature, :level,
                                 :allows_manual_entries, :is_active, :is_system, :initial_balance)
                            """), {
                                "business_id": business_id,
                                "code": acc_data["code"],
                                "name": acc_data["name"],
                                "description": acc_data.get("description", ""),
                                "account_type": account_type,
                                "nature": nature,
                                "level": acc_data.get("level", 1),
                                "allows_manual_entries": acc_data.get("allows_manual_entries", True),
                                "is_active": acc_data.get("is_active", True),
                                "is_system": acc_data.get("is_system", False),
                                "initial_balance": acc_data.get("initial_balance", 0)
                            })
                            conn.commit()
                            created_count += 1
                            print(f"  ✅ Cuenta '{acc_data['code']} - {acc_data['name']}' creada")
                        else:
                            print(f"  ℹ️  Cuenta '{acc_data['code']}' ya existe")
                
                print(f"  ✅ {created_count} cuentas creadas para el negocio {business_id}")
        
        print("\n✅ Migración de cuentas por defecto completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate()

