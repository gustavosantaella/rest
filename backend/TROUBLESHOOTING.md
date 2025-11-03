# 🔧 Solución de Problemas

## Error: "module 'bcrypt' has no attribute '__about__'"

### Descripción
Este error ocurre por incompatibilidad entre versiones de `passlib` y `bcrypt`.

### Solución

#### Opción 1: Script Automático (Recomendado)

**Windows:**
```bash
update_dependencies.bat
```

**Linux/Mac:**
```bash
chmod +x update_dependencies.sh
./update_dependencies.sh
```

#### Opción 2: Manual

```bash
# 1. Desinstalar versiones problemáticas
pip uninstall -y passlib bcrypt

# 2. Instalar versiones compatibles
pip install passlib==1.7.4
pip install bcrypt==4.0.1

# 3. Verificar instalación
pip list | grep -E "passlib|bcrypt"
```

#### Opción 3: Reinstalar todo

```bash
# Eliminar entorno virtual
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Crear nuevo entorno
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## Error: "password cannot be longer than 72 bytes"

### Descripción
Bcrypt tiene un límite de 72 bytes para contraseñas.

### Solución
Este error debería estar resuelto con las versiones correctas de bcrypt. Si persiste:

```python
# En app/utils/security.py
def get_password_hash(password: str) -> str:
    # Truncar si es necesario (aunque no debería ser común)
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)
```

---

## Error: "Could not connect to PostgreSQL"

### Descripción
El backend no puede conectarse a la base de datos.

### Solución

1. **Verificar que PostgreSQL esté corriendo:**
```bash
# Windows
net start postgresql-x64-14  # Ajusta la versión

# Linux
sudo service postgresql status
sudo service postgresql start

# Mac
brew services list
brew services start postgresql
```

2. **Verificar credenciales en `.env`:**
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/restaurant_db
```

3. **Crear la base de datos si no existe:**
```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE restaurant_db;

# Salir
\q
```

4. **Verificar permisos:**
```sql
-- En psql
GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO tu_usuario;
```

---

## Error: "ModuleNotFoundError: No module named 'app'"

### Descripción
Python no encuentra el módulo `app`.

### Solución

1. **Asegúrate de estar en el directorio correcto:**
```bash
cd backend
```

2. **Verifica que el entorno virtual esté activado:**
```bash
# Deberías ver (venv) al inicio de tu línea de comando
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **Ejecuta desde el directorio correcto:**
```bash
# Desde el directorio backend/
python run.py
```

---

## Error: Puerto 8000 ya en uso

### Descripción
Otro proceso está usando el puerto 8000.

### Solución

**Opción 1: Usar otro puerto**
```bash
uvicorn app.main:app --reload --port 8001
```

**Opción 2: Terminar el proceso existente**

Windows:
```bash
netstat -ano | findstr :8000
taskkill /PID [número] /F
```

Linux/Mac:
```bash
lsof -ti:8000 | xargs kill -9
```

---

## Error: "CORS policy blocked"

### Descripción
El frontend no puede hacer peticiones al backend.

### Solución

1. **Verificar configuración CORS en `app/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Si usas otro puerto en el frontend, agrégalo:**
```python
allow_origins=["http://localhost:4200", "http://localhost:4201"],
```

---

## Error: Token JWT expirado

### Descripción
El token de autenticación ha caducado.

### Solución

1. **Volver a iniciar sesión**

2. **Aumentar tiempo de expiración (solo desarrollo):**
```env
# En .env
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

---

## Error: Tablas no se crean automáticamente

### Descripción
Las tablas de la base de datos no existen.

### Solución

```bash
# Opción 1: Ejecutar script de inicialización
python init_db.py

# Opción 2: Usar Alembic (avanzado)
alembic upgrade head
```

---

## Problemas de Rendimiento

### Base de datos lenta

1. **Agregar índices:**
```sql
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_table ON orders(table_id);
CREATE INDEX idx_orders_user ON orders(user_id);
```

2. **Analizar consultas:**
```python
# Agregar logging en database.py
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Ver queries SQL
)
```

---

## Logs y Debug

### Habilitar logs detallados

En `run.py`:
```python
import logging

logging.basicConfig(level=logging.DEBUG)

uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="debug"
)
```

---

## Obtener Ayuda Adicional

1. **Revisar logs del servidor:**
   - Los errores aparecen en la consola donde ejecutaste `python run.py`

2. **Usar la documentación interactiva:**
   - http://localhost:8000/docs
   - Prueba los endpoints directamente

3. **Verificar versiones:**
```bash
python --version  # Debe ser 3.8+
pip list
```

4. **Reinstalar desde cero:**
```bash
# Eliminar entorno virtual
rm -rf venv

# Crear nuevo
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar BD
python init_db.py

# Ejecutar
python run.py
```

---

## Contacto

Si ninguna solución funciona:
- Revisa la documentación completa en README.md
- Verifica que tengas todas las versiones correctas
- Asegúrate de que PostgreSQL esté correctamente instalado y corriendo

