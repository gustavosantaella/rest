"""
Migración: Agregar business_id a users y reestructurar constraints
Esta migración convierte el sistema a multi-tenancy (múltiples negocios)
"""
import sys
import os
# Agregar el directorio backend al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine, text
from app.config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as connection:
        print("📋 Iniciando migración de multi-tenancy...")
        
        # 1. Agregar columna business_id
        print("1. Agregando columna business_id a users...")
        connection.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS business_id INTEGER;
        """))
        connection.commit()
        
        # 2. Obtener el primer negocio (si existe) para asignar a usuarios existentes
        print("2. Asignando negocio a usuarios existentes...")
        result = connection.execute(text("""
            SELECT id FROM business_configuration LIMIT 1;
        """))
        business = result.fetchone()
        
        if business:
            business_id = business[0]
            connection.execute(text("""
                UPDATE users 
                SET business_id = :business_id 
                WHERE business_id IS NULL;
            """), {"business_id": business_id})
            connection.commit()
            print(f"   ✓ Usuarios asignados al negocio ID: {business_id}")
        else:
            print("   ⚠ No hay negocios configurados aún")
        
        # 3. Eliminar constraint de unique en username
        print("3. Removiendo constraints unique globales...")
        try:
            connection.execute(text("""
                ALTER TABLE users DROP CONSTRAINT IF EXISTS users_username_key;
            """))
            connection.commit()
            print("   ✓ Removed users_username_key")
        except Exception as e:
            print(f"   - users_username_key: {e}")
        
        # 4. Eliminar constraint de unique en email
        try:
            connection.execute(text("""
                ALTER TABLE users DROP CONSTRAINT IF EXISTS users_email_key;
            """))
            connection.commit()
            print("   ✓ Removed users_email_key")
        except Exception as e:
            print(f"   - users_email_key: {e}")
        
        # 5. Eliminar constraint de unique en dni
        try:
            connection.execute(text("""
                ALTER TABLE users DROP CONSTRAINT IF EXISTS users_dni_key;
            """))
            connection.commit()
            print("   ✓ Removed users_dni_key")
        except Exception as e:
            print(f"   - users_dni_key: {e}")
        
        # 6. Crear índices compuestos (unique por negocio)
        print("4. Creando índices compuestos (unique por negocio)...")
        
        # Username único por negocio
        connection.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_business_username 
            ON users(business_id, username);
        """))
        connection.commit()
        print("   ✓ Creado idx_users_business_username")
        
        # Email único por negocio
        connection.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_business_email 
            ON users(business_id, email);
        """))
        connection.commit()
        print("   ✓ Creado idx_users_business_email")
        
        # 7. Agregar foreign key a business_configuration
        print("5. Agregando foreign key constraint...")
        try:
            connection.execute(text("""
                ALTER TABLE users 
                ADD CONSTRAINT fk_users_business 
                FOREIGN KEY (business_id) 
                REFERENCES business_configuration(id) 
                ON DELETE CASCADE;
            """))
            connection.commit()
            print("   ✓ Foreign key agregada")
        except Exception as e:
            print(f"   - Foreign key ya existe o error: {e}")
        
        print("\n✅ Migración completada: Sistema convertido a multi-tenancy")
        print("   - Cada usuario ahora pertenece a un negocio")
        print("   - Username y email son únicos POR negocio (no globalmente)")
        print("   - DNI ya no es único globalmente")

if __name__ == "__main__":
    migrate()

