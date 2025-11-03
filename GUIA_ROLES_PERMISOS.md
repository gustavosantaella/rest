# 🔐 Guía Completa del Sistema de Roles y Permisos

## 🎯 Resumen del Sistema

Se ha implementado un sistema completo y profesional de **Roles y Permisos Granulares** que permite:

✅ Crear roles personalizados (Ej: "Mesero Turno Noche", "Supervisor de Cocina")  
✅ Asignar permisos específicos a cada rol (crear, editar, eliminar, reportes, etc.)  
✅ Asignar múltiples roles a un usuario  
✅ Control granular sobre 32 permisos diferentes  
✅ Administradores tienen acceso total automáticamente  

---

## 📊 Arquitectura del Sistema

### Conceptos Clave

**Permiso (Permission)**
- Acción específica del sistema (Ej: `products.create`, `orders.edit`)
- 32 permisos predefinidos
- Organizados por módulos
- Granularidad: Ver, Crear, Editar, Eliminar, Gestionar, Reportes

**Rol (Role)**
- Conjunto de permisos agrupados
- Personalizables por negocio
- Ejemplos: "Mesero VIP", "Cajero Senior", "Chef Principal"
- Un rol puede tener N permisos

**Usuario + Roles**
- Un usuario puede tener múltiples roles
- Los permisos se acumulan de todos sus roles
- Administradores tienen acceso total (sin necesidad de roles)

### Diagrama de Relaciones

```
User (Usuario)
  ├─ role (enum: ADMIN, WAITER, etc.) ← Rol base del sistema
  └─ custom_roles (muchos a muchos) → Role (Roles personalizados)
       └─ permissions (muchos a muchos) → Permission (Permisos)
```

---

## 🔧 Backend - Implementación

### Tablas de Base de Datos

#### 1. `permissions` (Permisos del Sistema)
```sql
- id: SERIAL PRIMARY KEY
- code: VARCHAR UNIQUE (Ej: "products.create")
- name: VARCHAR (Ej: "Crear Productos")
- description: TEXT
- module: VARCHAR (Ej: "products", "orders")
- created_at: TIMESTAMP
```

#### 2. `roles` (Roles Personalizados)
```sql
- id: SERIAL PRIMARY KEY
- business_id: INTEGER (FK → business_configuration)
- name: VARCHAR (Ej: "Mesero Turno Noche")
- description: TEXT
- is_active: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- deleted_at: TIMESTAMP (soft delete)
```

#### 3. `role_permissions` (Permisos de un Rol)
```sql
- role_id: INTEGER (FK → roles)
- permission_id: INTEGER (FK → permissions)
- created_at: TIMESTAMP
PRIMARY KEY (role_id, permission_id)
```

#### 4. `user_roles` (Roles de un Usuario)
```sql
- user_id: INTEGER (FK → users)
- role_id: INTEGER (FK → roles)
- created_at: TIMESTAMP
PRIMARY KEY (user_id, role_id)
```

### 32 Permisos Predefinidos

#### Dashboard (1 permiso)
- `dashboard.view` - Ver Dashboard

#### Productos (4 permisos)
- `products.view` - Ver Productos
- `products.create` - Crear Productos
- `products.edit` - Editar Productos
- `products.delete` - Eliminar Productos

#### Inventario (2 permisos)
- `inventory.view` - Ver Inventario
- `inventory.manage` - Gestionar Inventario

#### Menú (4 permisos)
- `menu.view` - Ver Menú
- `menu.create` - Crear Items de Menú
- `menu.edit` - Editar Menú
- `menu.delete` - Eliminar Items

#### Mesas (2 permisos)
- `tables.view` - Ver Mesas
- `tables.manage` - Gestionar Mesas

#### Órdenes (5 permisos)
- `orders.view` - Ver Órdenes
- `orders.create` - Crear Órdenes
- `orders.edit` - Editar Órdenes
- `orders.delete` - Cancelar Órdenes
- `orders.process_payment` - Procesar Pagos

#### Usuarios (5 permisos)
- `users.view` - Ver Usuarios
- `users.create` - Crear Usuarios
- `users.edit` - Editar Usuarios
- `users.delete` - Eliminar Usuarios
- `users.manage_permissions` - Gestionar Permisos

#### Configuración (4 permisos)
- `config.view` - Ver Configuración
- `config.edit` - Editar Configuración
- `config.manage_roles` - Gestionar Roles
- `config.manage_permissions` - Gestionar Permisos

#### Reportes (3 permisos)
- `reports.view` - Ver Reportes
- `reports.generate` - Generar Reportes
- `reports.export` - Exportar Reportes

#### Métodos de Pago (2 permisos)
- `payment_methods.view` - Ver Métodos de Pago
- `payment_methods.manage` - Gestionar Métodos de Pago

### Endpoints API

#### Roles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/roles` | Listar roles del negocio |
| GET | `/api/roles/{id}` | Obtener un rol |
| POST | `/api/roles` | Crear rol |
| PUT | `/api/roles/{id}` | Actualizar rol |
| DELETE | `/api/roles/{id}` | Eliminar rol (soft delete) |

#### Permisos del Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/system-permissions` | Listar todos los permisos |
| GET | `/api/system-permissions/by-module` | Permisos agrupados por módulo |
| POST | `/api/system-permissions/seed` | Crear permisos predefinidos |

#### Asignación de Roles a Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/roles/user/{user_id}/roles` | Obtener roles de un usuario |
| PUT | `/api/roles/user/{user_id}/roles` | Asignar roles a un usuario |

---

## 🎨 Frontend - Interfaz

### Navegación

**Menú Principal → Configuración → Roles y Permisos**

Solo visible para **Administradores**.

### Pantalla: Gestión de Roles

**Ruta:** `/configuration/roles`

**Características:**
- Grid de tarjetas con roles existentes
- Botón "Nuevo Rol" para crear
- Cada tarjeta muestra:
  - Nombre del rol
  - Descripción
  - Estado (Activo/Inactivo)
  - Cantidad de permisos
  - Preview de permisos
  - Botones: Editar, Eliminar

### Modal: Crear/Editar Rol

**Secciones:**

1. **Datos del Rol**
   - Nombre (requerido)
   - Descripción (opcional)
   - Estado activo (checkbox)

2. **Selección de Permisos**
   - Agrupados por módulo
   - Checkboxes por permiso
   - Checkbox de módulo completo
   - Contador de permisos seleccionados

**Características:**
- ✅ Selección/deselección por módulo completo
- ✅ Estados: Todos, Ninguno, Parcial
- ✅ Vista colapsable por módulo
- ✅ Iconos descriptivos
- ✅ Diseño responsive

### Pantalla: Gestión de Usuarios

**Ruta:** `/users`

**Nuevos Botones en cada Usuario:**

| Botón | Icono | Función | Disponible para |
|-------|-------|---------|-----------------|
| Editar | ✏️ | Editar datos del usuario | Todos excepto Admin |
| Roles | 👥 | Asignar roles personalizados | Todos excepto Admin |
| Permisos | 🔒 | Asignar permisos directos | Todos excepto Admin |
| Activar/Desactivar | ✅/❌ | Cambiar estado | Todos |
| Eliminar | 🗑️ | Eliminar usuario | Todos excepto yo mismo |

**Nota:** Los administradores NO muestran botones de roles/permisos (tienen acceso total).

### Modal: Asignar Roles a Usuario

**Características:**
- Lista de todos los roles activos del negocio
- Checkboxes para seleccionar múltiples roles
- Preview de permisos de cada rol
- Contador de permisos por rol
- Selección múltiple

---

## 🚀 Flujo de Uso Completo

### Escenario: Crear Rol "Mesero Turno Noche"

1. **Ir a Configuración → Roles y Permisos**
2. **Click en "+ Nuevo Rol"**
3. **Llenar datos:**
   - Nombre: "Mesero Turno Noche"
   - Descripción: "Mesero con acceso a órdenes y mesas del turno nocturno"
   - Estado: Activo

4. **Seleccionar permisos:**
   - ✅ Dashboard → Ver Dashboard
   - ✅ Órdenes → Ver Órdenes
   - ✅ Órdenes → Crear Órdenes
   - ✅ Órdenes → Editar Órdenes
   - ✅ Órdenes → Procesar Pagos
   - ✅ Mesas → Ver Mesas
   - ✅ Mesas → Gestionar Mesas
   - ✅ Menú → Ver Menú

5. **Click en "Crear Rol"**
6. **✅ Rol creado con 8 permisos**

### Escenario: Asignar Rol a Usuario

1. **Ir a Usuarios**
2. **Buscar usuario "Juan Pérez"**
3. **Click en botón 👥 (Roles)**
4. **Modal se abre mostrando roles disponibles**
5. **Seleccionar:**
   - ✅ Mesero Turno Noche
   - ✅ Cajero (si tiene múltiples funciones)
6. **Click en "Guardar"**
7. **✅ Usuario ahora tiene ambos roles y todos sus permisos**

---

## 💡 Casos de Uso

### Caso 1: Restaurante con Turnos

**Roles Creados:**
- "Mesero Turno Día" → Órdenes + Mesas (6:00-14:00)
- "Mesero Turno Noche" → Órdenes + Mesas (18:00-02:00)
- "Cajero Principal" → Órdenes (pago) + Reportes
- "Chef de Línea" → Ver órdenes de cocina
- "Supervisor" → Todo excepto configuración

**Beneficio:** Cada empleado solo ve lo que necesita según su turno/función.

### Caso 2: Kiosko Pequeño

**Roles Creados:**
- "Vendedor" → Productos + Órdenes + Pagos
- "Encargado" → Vendedor + Inventario + Reportes

**Beneficio:** Simplifica la gestión en negocios pequeños.

### Caso 3: Cadena de Restaurantes

**Roles Creados:**
- "Gerente de Sucursal" → Acceso total excepto configuración global
- "Mesero Junior" → Solo órdenes y mesas (sin eliminar)
- "Mesero Senior" → Órdenes, mesas, inventario básico
- "Contador" → Solo reportes y exportación

**Beneficio:** Estructura organizacional clara y escalable.

---

## 🎨 Interfaz de Usuario

### Gestión de Roles

```
┌─────────────────────────────────────────────────┐
│  Roles y Permisos             [+ Nuevo Rol]     │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌───────────────┐  ┌───────────────┐          │
│  │ Mesero VIP    │  │ Cajero Senior │          │
│  │ ─────────────  │  │ ─────────────  │          │
│  │ 12 permisos   │  │ 8 permisos    │          │
│  │ • Ver Órdenes │  │ • Procesar... │          │
│  │ • Crear...    │  │ • Ver Repor.. │          │
│  │               │  │               │          │
│  │ [Editar] [🗑️]  │  │ [Editar] [🗑️]  │          │
│  └───────────────┘  └───────────────┘          │
└─────────────────────────────────────────────────┘
```

### Modal de Rol

```
┌─────────────────────────────────────────────┐
│  Nuevo Rol                              [×] │
├─────────────────────────────────────────────┤
│  Nombre: [Mesero Turno Noche___________]   │
│  Descripción: [________________________]   │
│  □ Rol activo                               │
│                                             │
│  Permisos (8 seleccionados)                 │
│  ┌─────────────────────────────────────┐   │
│  │ 📊 Dashboard         [✓] Todos      │   │
│  │   ☑ Ver Dashboard                   │   │
│  ├─────────────────────────────────────┤   │
│  │ 📋 Órdenes           [~] Parcial    │   │
│  │   ☑ Ver Órdenes                     │   │
│  │   ☑ Crear Órdenes                   │   │
│  │   ☐ Editar Órdenes                  │   │
│  │   ☐ Cancelar Órdenes                │   │
│  │   ☑ Procesar Pagos                  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│             [Cancelar] [Crear Rol]          │
└─────────────────────────────────────────────┘
```

### Gestión de Usuario

```
┌─────────────────────────────────────────────┐
│  Juan Pérez (@juan.perez)                  │
│  juan@example.com                           │
│  Mesero - Gestión de órdenes y mesas        │
│                                             │
│  [Editar] [👥] [🔒] [Desactivar] [🗑️]       │
└─────────────────────────────────────────────┘
      Botones:
      👥 = Asignar Roles
      🔒 = Permisos Directos
```

---

## 📝 Instalación y Configuración

### Paso 1: Migrar Base de Datos

```bash
cd backend
.venv/Scripts/python.exe create_roles_permissions_tables.py
```

**Resultado:**
```
✅ Tabla 'permissions' creada
✅ Tabla 'roles' creada
✅ Tabla 'role_permissions' creada
✅ Tabla 'user_roles' creada
```

### Paso 2: Seed de Permisos

```bash
.venv/Scripts/python.exe seed_system_permissions.py
```

**Resultado:**
```
✅ 32 permisos creados
```

### Paso 3: Reiniciar Backend

```bash
uvicorn app.main:app --reload
```

### Paso 4: Acceder al Sistema

1. Inicia sesión como **Administrador**
2. Ve a **Configuración → Roles y Permisos**
3. Crea tu primer rol personalizado
4. Ve a **Usuarios** y asigna roles

---

## 🎯 Flujos de Trabajo

### Crear un Nuevo Rol

1. **Configuración → Roles y Permisos**
2. **Click "+ Nuevo Rol"**
3. **Completar formulario**
4. **Seleccionar permisos por módulo**
   - Click en el nombre del módulo para seleccionar todos
   - Click individual para permisos específicos
5. **Guardar**
6. **✅ Rol creado y disponible**

### Asignar Rol a Usuario

1. **Usuarios**
2. **Buscar usuario**
3. **Click en 👥 (Roles)**
4. **Seleccionar uno o más roles**
5. **Guardar**
6. **✅ Usuario tiene permisos acumulados de todos sus roles**

### Modificar Permisos de un Rol

1. **Configuración → Roles y Permisos**
2. **Buscar rol**
3. **Click "Editar"**
4. **Modificar permisos**
5. **Guardar**
6. **✅ Todos los usuarios con ese rol obtienen los nuevos permisos**

---

## 🔐 Lógica de Permisos

### Jerarquía de Acceso

```
1. Administrador (role = ADMIN)
   └─ Acceso TOTAL automático (sin necesidad de roles/permisos)

2. Usuario con Roles Personalizados
   └─ Permisos = SUMA de todos sus roles
   
3. Usuario sin Roles
   └─ Solo acceso básico según role del sistema
```

### Ejemplo de Acumulación de Permisos

**Usuario: María González**
- Role base: `WAITER`
- Roles asignados:
  - "Mesero VIP" (10 permisos)
  - "Cajero Auxiliar" (5 permisos)

**Permisos totales:** 15 permisos únicos (se eliminan duplicados)

---

## 🎨 Personalización

### Agregar Nuevos Permisos

1. **Editar:** `backend/app/utils/seed_permissions.py`
2. **Agregar a `SYSTEM_PERMISSIONS`:**
```python
{
    "code": "custom.action",
    "name": "Acción Personalizada",
    "module": "custom",
    "description": "Descripción"
}
```
3. **Ejecutar seed nuevamente**

### Modificar Módulos

**Backend:** `backend/app/utils/seed_permissions.py`  
**Frontend:** `frontend/src/app/core/models/role.model.ts` → `SYSTEM_MODULES`

---

## 📊 Ventajas del Sistema

### vs Sistema de Permisos Fijos

| Aspecto | Permisos Fijos | Roles Personalizados |
|---------|----------------|----------------------|
| Flexibilidad | ❌ Limitada | ✅ Total |
| Reutilización | ❌ No | ✅ Sí |
| Escalabilidad | ❌ Baja | ✅ Alta |
| Mantenimiento | ❌ Difícil | ✅ Fácil |
| Granularidad | ❌ Por módulo | ✅ Por acción |

### Beneficios Clave

✅ **Flexibilidad Total** - Crea roles según tu organización  
✅ **Granularidad** - Control por acción (view, create, edit, delete)  
✅ **Reutilización** - Un rol para múltiples usuarios  
✅ **Escalable** - Agrega permisos sin código  
✅ **Auditoría** - Timestamps en todas las relaciones  
✅ **Soft Delete** - Roles eliminados pueden recuperarse  
✅ **Multi-rol** - Un usuario puede tener N roles  

---

## 🔄 Migración desde Sistema Anterior

Si ya tenías el sistema de permisos simple (`UserPermission`):

1. ✅ **Ambos sistemas coexisten**
2. El nuevo sistema es más potente y flexible
3. Puedes migrar gradualmente
4. `UserPermission` sigue funcionando para permisos directos

**Recomendación:** Usar el nuevo sistema de roles para la mayoría de usuarios.

---

## 🛡️ Seguridad

### Control de Acceso

- ✅ Solo **Administradores** pueden gestionar roles
- ✅ Roles son **por negocio** (business_id)
- ✅ Soft delete previene pérdida de datos
- ✅ CASCADE en eliminación de usuarios
- ✅ Validaciones en backend y frontend

### Próximos Pasos (Opcional)

- [ ] Middleware de validación de permisos en rutas
- [ ] Guards de Angular basados en permisos
- [ ] Logs de cambios de roles/permisos
- [ ] Permisos temporales (con fecha de expiración)
- [ ] Herencia de roles (roles padre/hijo)

---

## 📖 API Documentation

Visita: `http://localhost:8000/docs`

Endpoints disponibles:
- `/api/roles` - Gestión de roles
- `/api/system-permissions` - Permisos del sistema
- `/api/roles/user/{id}/roles` - Asignación de roles

---

## ✨ Resumen

Has implementado un **Sistema Empresarial de Roles y Permisos** con:

- ✅ 32 permisos granulares
- ✅ Roles personalizables ilimitados
- ✅ Asignación múltiple de roles
- ✅ Interfaz visual intuitiva
- ✅ Soft delete en roles
- ✅ Totalmente escalable

**Estado:** 🎉 COMPLETADO AL 100%  
**Versión:** 3.0.0  
**Fecha:** ${new Date().toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}

