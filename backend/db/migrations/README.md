# Database Migrations

Esta carpeta contiene todos los scripts de migración de la base de datos PostgreSQL.

## 📋 Orden de Ejecución de Migraciones

Las migraciones deben ejecutarse en el siguiente orden:

1. `migrate_add_profile_fields.py` - Agrega campos de perfil a usuarios
2. `migrate_add_payment_methods.py` - Crea tabla de métodos de pago
3. `migrate_add_customer_fields.py` - Agrega campos de cliente a órdenes
4. `migrate_add_order_payments.py` - Crea tabla de pagos de órdenes
5. `migrate_add_show_in_catalog.py` - Agrega flag de catálogo a productos
6. `migrate_fix_show_in_catalog_type.py` - Corrige tipo de dato del flag
7. `migrate_add_image_url_to_products.py` - Agrega URL de imagen a productos
8. `migrate_add_slug_to_business.py` - Agrega slug a configuración del negocio

## 🚀 Cómo Ejecutar una Migración

### Desde la raíz del backend:

```bash
# Windows (con virtual env activado)
.venv\Scripts\python.exe db/migrations/migrate_add_profile_fields.py

# Linux/Mac (con virtual env activado)
.venv/bin/python db/migrations/migrate_add_profile_fields.py
```

### O usando rutas absolutas:

```bash
cd C:/laragon/www/ecommerce/backend
.venv/Scripts/python.exe db/migrations/nombre_migracion.py
```

## ⚠️ Notas Importantes

1. **Ejecuta las migraciones en orden** - Algunas dependen de cambios previos
2. **Haz backup antes** - Siempre respalda tu base de datos antes de migrar
3. **Una sola vez** - No ejecutes la misma migración dos veces
4. **Verifica el resultado** - Cada migración imprime mensajes de confirmación

## 📝 Crear una Nueva Migración

Si necesitas crear una nueva migración:

```python
from sqlalchemy import create_engine, text
from app.config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as connection:
        print("Ejecutando migración...")
        
        # Tu código SQL aquí
        connection.execute(text("""
            ALTER TABLE tu_tabla 
            ADD COLUMN nuevo_campo VARCHAR;
        """))
        
        connection.commit()
        print("✅ Migración completada")

if __name__ == "__main__":
    migrate()
```

## 🔍 Verificar Estado de la Base de Datos

Para verificar qué columnas tiene una tabla:

```sql
-- PostgreSQL
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'nombre_tabla';
```

