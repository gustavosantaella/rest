# 🔄 Guía de Migración de Base de Datos

## 🎯 ¿Cuándo Necesitas Migrar?

Cuando ves errores como:
```
sqlalchemy.exc.ProgrammingError: column users.dni does not exist
```

Esto significa que el **modelo de Python** tiene campos nuevos que **no existen en la base de datos**.

## ✅ Solución Rápida

### Windows:
```bash
cd backend
migrate_add_profile_fields.bat
```

### Linux/Mac:
```bash
cd backend
chmod +x migrate_add_profile_fields.sh
./migrate_add_profile_fields.sh
```

### O manualmente:
```bash
cd backend
python migrate_add_profile_fields.py
```

## 📋 Deberías Ver:

```
==================================================
MIGRACIÓN: Agregar Campos de Perfil
==================================================

🔧 Agregando campos de perfil a la tabla users...
✅ Columna 'dni' agregada
✅ Columna 'country' agregada
✅ Índice para 'dni' creado

✨ Migración completada exitosamente!
💡 Ahora puedes ejecutar: python run.py
```

## 🔧 ¿Qué Hace la Migración?

Agrega estos campos a la tabla `users`:
- `dni` VARCHAR UNIQUE - Documento de identidad
- `country` VARCHAR - País del usuario
- Índice para búsquedas rápidas por DNI

## 🚀 Después de Migrar

1. **Ejecuta el backend:**
```bash
python run.py
```

2. **Verifica que funcione:**
- El login debe funcionar correctamente
- Puedes acceder a "Mi Perfil"
- Puedes actualizar DNI y país

## 🔄 Alternativa: Recrear Base de Datos

Si prefieres empezar de cero (⚠️ PERDERÁS TODOS LOS DATOS):

### Opción 1: Desde PostgreSQL
```bash
# Conectar a PostgreSQL
psql -U postgres

# Eliminar base de datos
DROP DATABASE restaurant_db;

# Crear de nuevo
CREATE DATABASE restaurant_db;

# Salir
\q

# Ejecutar backend (creará tablas automáticamente)
python run.py
```

### Opción 2: Desde Python
```python
# En Python
from app.database import engine, Base

# Eliminar todas las tablas
Base.metadata.drop_all(bind=engine)

# Crear todas las tablas de nuevo
Base.metadata.create_all(bind=engine)
```

## 📊 Migraciónes Futuras con Alembic

Para un sistema de migración más robusto:

### Instalar Alembic:
```bash
pip install alembic
```

### Inicializar:
```bash
alembic init alembic
```

### Configurar:
Editar `alembic.ini`:
```ini
sqlalchemy.url = postgresql://user:password@localhost:5432/restaurant_db
```

### Crear Migración:
```bash
alembic revision --autogenerate -m "Add dni and country to users"
```

### Aplicar Migración:
```bash
alembic upgrade head
```

## 🐛 Solución de Problemas

### Error: "Permission denied"
```bash
# Linux/Mac
chmod +x migrate_add_profile_fields.sh
sudo ./migrate_add_profile_fields.sh
```

### Error: "Could not connect to database"
```bash
# Verifica que PostgreSQL esté corriendo
sudo service postgresql status  # Linux
brew services list  # Mac
```

### Error: "Database does not exist"
```bash
# Crear la base de datos
createdb restaurant_db
```

### Error: "Column already exists"
```
✅ Esto es OK - La migración es idempotente
✅ Puedes ejecutarla múltiples veces sin problemas
```

## 📝 Notas Importantes

1. **Backup**: Siempre haz backup antes de migrar en producción
2. **Testing**: Prueba primero en desarrollo
3. **Idempotente**: El script usa `IF NOT EXISTS` para seguridad
4. **Sin pérdida de datos**: Esta migración NO borra datos
5. **Reversible**: Puedes quitar las columnas si es necesario

## 🎯 Checklist Post-Migración

- [ ] Migración ejecutada sin errores
- [ ] Backend inicia correctamente (python run.py)
- [ ] Login funciona
- [ ] "Mi Perfil" carga sin errores
- [ ] Puedes actualizar DNI y país
- [ ] No hay errores en consola

---

**¡Ejecuta la migración y todo funcionará!** ✅

