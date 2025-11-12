# Guía de Migración: Multi-Tenancy por business_id

## 📋 ¿Qué cambió?

Se agregó el campo `business_id` a los siguientes modelos para implementar multi-tenancy (aislamiento de datos por negocio):

### Modelos Actualizados:
- ✅ **tables** - Mesas del restaurante
- ✅ **orders** - Órdenes
- ✅ **products** - Productos
- ✅ **categories** - Categorías de productos
- ✅ **menu_items** - Items del menú
- ✅ **menu_categories** - Categorías del menú

### Modelos que YA tenían business_id:
- ✅ customers
- ✅ payment_methods
- ✅ account_receivable
- ✅ account_payable
- ✅ users

## 🚀 Cómo Aplicar la Migración

### Paso 1: Backup de la Base de Datos
```bash
# PostgreSQL
pg_dump -U tu_usuario restaurant_db > backup_$(date +%Y%m%d).sql

# SQLite
cp db/restaurant.db db/restaurant_backup_$(date +%Y%m%d).db
```

### Paso 2: Ejecutar el Script de Migración
```bash
cd backend
python add_business_id_migration.py
```

El script te pedirá confirmación y luego:
1. Agregará la columna `business_id` a las tablas
2. Asignará un `business_id` por defecto a los datos existentes
3. Creará foreign keys y índices
4. Establecerá la columna como NOT NULL

### Paso 3: Verificar la Migración
```bash
# Verificar que las columnas se agregaron correctamente
psql -U tu_usuario restaurant_db -c "\d tables"
psql -U tu_usuario restaurant_db -c "\d products"
psql -U tu_usuario restaurant_db -c "\d orders"
```

## 📝 Cambios en los Servicios

### Antes:
```python
# Obtener todas las mesas (sin filtro)
tables = db.query(Table).all()
```

### Después:
```python
# Obtener solo las mesas del negocio del usuario
tables = db.query(Table).filter(
    Table.business_id == current_user.business_id
).all()
```

## ✅ Módulos PyNest Ya Actualizados

Los siguientes módulos PyNest ya están configurados para filtrar por `business_id`:

- ✅ **TablesService** - Todas las operaciones filtradas
- ✅ **ProductsService** - Productos y categorías filtradas
- ✅ **CustomersService** - Ya tenía el filtro
- ✅ **UsersService** - Ya tenía el filtro

## ⚠️ Acciones Pendientes

Si usas los routers legacy, necesitas actualizarlos para filtrar por `business_id`. Por ejemplo:

### Router Legacy de Orders (necesita actualización):
```python
# ❌ Antes - Sin filtro
orders = db.query(Order).all()

# ✅ Después - Con filtro
orders = db.query(Order).filter(
    Order.business_id == current_user.business_id
).all()
```

## 🔍 Verificación Post-Migración

### 1. Prueba la Creación:
```bash
# Crear una mesa
curl -X POST "http://localhost:8000/api/tables" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"number": "1", "capacity": 4}'
```

### 2. Verifica el Aislamiento:
- Crea dos negocios diferentes
- Crea mesas/productos en cada uno
- Verifica que cada usuario solo vea los datos de su negocio

### 3. Prueba los Endpoints:
- GET /api/tables
- GET /api/products
- GET /api/orders
- GET /api/customers

## 🐛 Solución de Problemas

### Error: "column business_id does not exist"
**Solución**: Ejecuta el script de migración:
```bash
python add_business_id_migration.py
```

### Error: "null value in column business_id violates not-null constraint"
**Problema**: Datos sin business_id asignado

**Solución**:
```sql
-- Asignar business_id por defecto
UPDATE tables SET business_id = 1 WHERE business_id IS NULL;
UPDATE products SET business_id = 1 WHERE business_id IS NULL;
UPDATE orders SET business_id = (
    SELECT business_id FROM users WHERE users.id = orders.user_id
) WHERE business_id IS NULL;
```

### Los Datos No Se Aíslan Correctamente
**Verifica**:
1. Que el usuario tenga `business_id` asignado
2. Que las consultas incluyan el filtro `Table.business_id == current_user.business_id`
3. Que estés usando los servicios PyNest actualizados

## 📊 Estructura de la Base de Datos

### Tabla: tables
```sql
CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES business_configuration(id),
    number VARCHAR NOT NULL,
    capacity INTEGER NOT NULL,
    status VARCHAR,
    location VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    INDEX idx_tables_business_id (business_id)
);
```

### Tabla: products
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES business_configuration(id),
    name VARCHAR NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    purchase_price FLOAT,
    sale_price FLOAT,
    stock FLOAT,
    -- ... otros campos
    INDEX idx_products_business_id (business_id)
);
```

## 🎯 Beneficios

1. **Seguridad**: Cada negocio solo accede a sus propios datos
2. **Escalabilidad**: Múltiples negocios en la misma base de datos
3. **Simplicidad**: Sin necesidad de bases de datos separadas
4. **Performance**: Índices optimizados por business_id

## 📚 Referencias

- Modelos actualizados: `backend/app/models/`
- Servicios PyNest: `backend/app/nest_modules/`
- Script de migración: `backend/add_business_id_migration.py`

---

**Fecha de Migración**: 2025
**Versión**: 2.0.0

