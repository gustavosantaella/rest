# 🚀 Guía de Inicio Rápido

## 📋 Credenciales de Acceso

Al iniciar el sistema, se crea automáticamente un usuario administrador:

```
Usuario:  admin
Email:    admin@admin.admin
Password: 123456.Ab!
Rol:      Administrador
```

> ⚠️ **Seguridad:** Cambia esta contraseña después del primer inicio de sesión.

## ⚡ Inicio Rápido (3 Pasos)

### 1️⃣ Backend

```bash
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos en .env
echo "DATABASE_URL=postgresql://user:password@localhost:5432/restaurant_db" > .env

# Crear base de datos
createdb restaurant_db

# Inicializar (crea tablas y usuario admin)
python init_db.py

# Ejecutar
python run.py
```

✅ Backend listo en: http://localhost:8000

### 2️⃣ Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar
npm start
```

✅ Frontend listo en: http://localhost:4200

### 3️⃣ Acceder al Sistema

1. Abre http://localhost:4200
2. Ingresa las credenciales:
   - **Usuario:** `admin`
   - **Password:** `123456.Ab!`
3. ¡Listo! Ya puedes usar el sistema

## 📦 Primeros Pasos Después del Login

### 1. Crear Categorías de Productos
- Ve a **Inventario**
- Click en "Nueva Categoría"
- Ejemplos: Bebidas, Comidas, Postres, etc.

### 2. Agregar Productos
- En **Inventario**, click en "Nuevo Producto"
- Completa la información:
  - Nombre (ej: Coca-Cola 500ml)
  - Categoría
  - Unidad de medida (unidad, kg, litro, etc.)
  - Precio de compra y venta
  - Stock inicial

### 3. Configurar Mesas
- Ve a **Mesas**
- Click en "Nueva Mesa"
- Asigna número y capacidad
- Opcional: ubicación (terraza, interior, etc.)

### 4. Crear Usuarios del Personal
- Ve a **Usuarios** (solo Admin)
- Click en "Nuevo Usuario"
- Asigna rol según su función:
  - **Admin:** Acceso total
  - **Manager:** Gestión de inventario y personal
  - **Waiter:** Tomar órdenes
  - **Cashier:** Procesar pagos

### 5. Crear Tu Primera Orden
- Ve a **Órdenes**
- Click en "Nueva Orden"
- Selecciona una mesa (opcional)
- Agrega productos
- Click en "Crear Orden"

## 🔧 Solución de Problemas Comunes

### Error: No se puede conectar a PostgreSQL
```bash
# Asegúrate de que PostgreSQL esté corriendo
sudo service postgresql start  # Linux
brew services start postgresql  # Mac
```

### Error: Puerto 8000 o 4200 en uso
```bash
# Backend en otro puerto
uvicorn app.main:app --reload --port 8001

# Frontend en otro puerto
ng serve --port 4201
```

### Error: No aparecen datos
- Verifica que el backend esté corriendo
- Revisa la URL de la API en `frontend/src/environments/environment.ts`
- Debe ser: `http://localhost:8000/api`

## 📱 Accesos Directos

- 🏠 **Dashboard:** http://localhost:4200/dashboard
- 📦 **Inventario:** http://localhost:4200/inventory
- 🍽️ **Mesas:** http://localhost:4200/tables
- 🧾 **Órdenes:** http://localhost:4200/orders
- 👥 **Usuarios:** http://localhost:4200/users
- 📚 **API Docs:** http://localhost:8000/docs

## 💡 Tips Útiles

1. **Stock Bajo:** El sistema alerta cuando el stock está por debajo del mínimo configurado
2. **Cambio de Estado:** Las mesas cambian automáticamente a "Ocupada" al crear una orden
3. **Cálculo Automático:** Los totales e impuestos se calculan automáticamente
4. **Múltiples Unidades:** Puedes vender por unidad, peso o volumen según el producto

## 📞 ¿Necesitas Ayuda?

- Revisa el [README.md](README.md) completo
- Consulta la [documentación del backend](backend/README.md)
- Consulta la [documentación del frontend](frontend/README.md)
- Explora la API interactiva en http://localhost:8000/docs

---

**¡Disfruta usando el sistema! 🎉**

