# Módulo de Clientes

## 📋 Descripción

El módulo de clientes permite registrar y gestionar la información de los clientes del negocio. Es completamente opcional y útil para llevar un registro de clientes habituales.

## 🎯 Características

### Campos del Cliente
- **Nombre** (requerido): Nombre del cliente
- **Apellido** (opcional): Apellido del cliente
- **DNI/Cédula** (opcional): Documento de identidad
- **Teléfono** (opcional): Número de contacto
- **Correo** (opcional): Email del cliente

### Funcionalidades
- ✅ Crear nuevos clientes
- ✅ Editar información de clientes
- ✅ Eliminar clientes (soft delete)
- ✅ Buscar clientes por cualquier campo
- ✅ Vista de tarjetas con información del cliente
- ✅ Validación de DNI duplicado en el mismo negocio

## 🚀 Instalación

### Backend

1. **La migración ya fue ejecutada**, pero si necesitas ejecutarla manualmente:
```bash
cd backend
source .venv/Scripts/activate  # En Windows con Git Bash
python db/migrations/migrate_add_customers_table.py
```

2. **Verificar que el backend esté corriendo**:
```bash
cd backend
source .venv/Scripts/activate
python run.py
```

El backend estará disponible en: `http://localhost:8000`

### Frontend

1. **Instalar dependencias** (si no están instaladas):
```bash
cd frontend
npm install
```

2. **Ejecutar el frontend**:
```bash
cd frontend
npm start
```

El frontend estará disponible en: `http://localhost:4200`

## 📱 Uso

### Acceder al Módulo

1. Inicia sesión en tu aplicación
2. En el menú lateral, haz clic en **"Clientes"** (ícono de personas)
3. Verás la lista de clientes registrados

### Crear un Cliente

1. Haz clic en el botón **"+ Nuevo Cliente"**
2. Completa el formulario:
   - **Nombre**: Campo obligatorio
   - **Apellido**: Campo opcional
   - **DNI/Cédula**: Campo opcional (se valida que no esté duplicado)
   - **Teléfono**: Campo opcional
   - **Correo**: Campo opcional (se valida formato de email)
3. Haz clic en **"Guardar"**

### Buscar un Cliente

1. Usa la barra de búsqueda en la parte superior
2. Puedes buscar por:
   - Nombre
   - Apellido
   - DNI
   - Teléfono
   - Correo electrónico

### Editar un Cliente

1. Haz clic en el botón **"Editar"** en la tarjeta del cliente
2. Modifica los campos necesarios
3. Haz clic en **"Guardar"**

### Eliminar un Cliente

1. Haz clic en el ícono de **papelera** 🗑️ en la tarjeta del cliente
2. Confirma la eliminación en el diálogo
3. El cliente se eliminará (soft delete, no se borra físicamente)

## 🔧 Estructura Técnica

### Backend (FastAPI)

**Archivos creados:**
- `backend/app/models/customer.py` - Modelo de base de datos
- `backend/app/schemas/customer.py` - Schemas de validación
- `backend/app/routers/customers.py` - Endpoints API
- `backend/db/migrations/migrate_add_customers_table.py` - Migración de BD

**Endpoints disponibles:**
- `GET /api/customers` - Listar clientes (con búsqueda opcional)
- `POST /api/customers` - Crear cliente
- `GET /api/customers/{id}` - Obtener cliente por ID
- `PUT /api/customers/{id}` - Actualizar cliente
- `DELETE /api/customers/{id}` - Eliminar cliente (soft delete)

### Frontend (Angular 19)

**Archivos creados:**
- `frontend/src/app/core/models/customer.model.ts` - Interfaces TypeScript
- `frontend/src/app/core/services/customer.service.ts` - Servicio API
- `frontend/src/app/features/customers/customers.component.ts` - Componente
- `frontend/src/app/features/customers/customers.component.html` - Template
- `frontend/src/app/features/customers/customers.component.scss` - Estilos

**Ruta:**
- `/customers` - Acceso al módulo de clientes

## 🔐 Seguridad

- Los clientes están asociados al negocio (`business_id`)
- Cada negocio solo puede ver sus propios clientes
- Requiere autenticación para acceder al módulo
- Soft delete: Los clientes eliminados no se borran físicamente

## 📊 Base de Datos

**Tabla:** `customers`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único (PK) |
| business_id | Integer | ID del negocio (FK) |
| nombre | String | Nombre del cliente (requerido) |
| apellido | String | Apellido (opcional) |
| dni | String | Documento de identidad (opcional) |
| telefono | String | Teléfono (opcional) |
| correo | String | Email (opcional) |
| created_at | DateTime | Fecha de creación |
| updated_at | DateTime | Fecha de actualización |
| deleted_at | DateTime | Fecha de eliminación (soft delete) |

**Índices:**
- `idx_customers_business_id` - Para filtrar por negocio
- `idx_customers_nombre` - Para búsquedas por nombre
- `idx_customers_dni` - Para búsquedas por DNI

## 🎨 Interfaz

La interfaz incluye:
- 🎴 Vista de tarjetas con información resumida
- 🔍 Búsqueda en tiempo real
- 📝 Formulario modal para crear/editar
- 🗑️ Confirmación de eliminación
- ✨ Animaciones y transiciones suaves
- 📱 Diseño responsive (mobile-friendly)
- 🎯 Tooltips informativos

## 📝 Notas

- El único campo obligatorio es el **nombre**
- El sistema valida que no haya DNIs duplicados en el mismo negocio
- El correo electrónico se valida automáticamente
- Los clientes se ordenan por fecha de creación (más recientes primero)
- El soft delete permite recuperar clientes eliminados accidentalmente (modificando la BD)

## 🔮 Mejoras Futuras (Opcional)

Posibles extensiones del módulo:
- Historial de compras del cliente
- Puntos de fidelidad
- Descuentos personalizados
- Exportación de datos a Excel/PDF
- Importación masiva de clientes
- Estadísticas de clientes frecuentes
- Integración con sistema de órdenes

---

**Última actualización:** 9 de noviembre de 2025

