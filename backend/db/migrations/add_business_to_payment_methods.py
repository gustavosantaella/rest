"""
Migración para agregar business_id a payment_methods
Los métodos de pago deben ser específicos por negocio
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import text
from app.database import engine

def migrate():
    print("Iniciando migración...")
    
    try:
        with engine.begin() as conn:
            # 1. Agregar business_id como columna nullable primero
            print("1. Agregando business_id a payment_methods...")
            conn.execute(text("""
                ALTER TABLE payment_methods 
                ADD COLUMN IF NOT EXISTS business_id INTEGER;
            """))
            
            # 2. Obtener el primer negocio (para asignar métodos existentes)
            print("2. Obteniendo primer negocio...")
            result = conn.execute(text("SELECT id FROM business_configuration LIMIT 1")).first()
            
            if result:
                first_business_id = result[0]
                print(f"   Primer negocio ID: {first_business_id}")
                
                # 3. Asignar métodos existentes al primer negocio
                print("3. Asignando métodos existentes al primer negocio...")
                conn.execute(text(f"""
                    UPDATE payment_methods 
                    SET business_id = {first_business_id}
                    WHERE business_id IS NULL;
                """))
            
            # 4. Hacer business_id NOT NULL
            print("4. Haciendo business_id NOT NULL...")
            conn.execute(text("""
                ALTER TABLE payment_methods 
                ALTER COLUMN business_id SET NOT NULL;
            """))
            
            # 5. Agregar foreign key constraint
            print("5. Agregando foreign key constraint...")
            conn.execute(text("""
                ALTER TABLE payment_methods 
                ADD CONSTRAINT fk_payment_methods_business 
                FOREIGN KEY (business_id) REFERENCES business_configuration(id) ON DELETE CASCADE;
            """))
            
            # 6. Crear índice para mejor performance
            print("6. Creando índice...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_payment_methods_business_id 
                ON payment_methods(business_id);
            """))
            
        print("✅ Migración completada exitosamente!")
        print("\nCambios realizados:")
        print("  - business_id agregado a payment_methods")
        print("  - Métodos existentes asignados al primer negocio")
        print("  - Foreign key constraint agregado")
        print("  - Índice creado para mejor performance")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    migrate()

