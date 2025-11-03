# 🔒 Sistema de Permisos por Módulos

## Implementación Completada

Se ha implementado un sistema completo de permisos granulares que permite a los administradores controlar el acceso de cada usuario a los diferentes módulos del sistema.

---

## 📋 Módulos con Control de Permisos

Los siguientes módulos pueden ser habilitados/deshabilitados por usuario:

| Módulo | Descripción | Icono |
|--------|-------------|-------|
| **Dashboard** | Panel principal con estadísticas | 📊 |
| **Inventario** | Gestión de inventario | 📦 |
| **Productos** | Gestión de productos | 🏷️ |
| **Menú** | Gestión del menú del restaurante | 🍽️ |
| **Mesas** | Gestión de mesas | 🪑 |
| **Órdenes** | Gestión de órdenes | 📋 |
| **Usuarios** | Gestión de usuarios | 👥 |
| **Configuración** | Configuración del negocio | ⚙️ |
| **Reportes** | Acceso a reportes | 📈 |

---

## 🔧 Backend - Implementación

### Modelo: `UserPermission`

**Ubicación:** `backend/app/models/permission.py`

**Campos:**
```python
- id: int
- user_id: int (FK a users)
- can_access_dashboard: bool (default: True)
- can_access_inventory: bool (default: False)
- can_access_products: bool (default: False)
- can_access_menu: bool (default: False)
- can_access_tables: bool (default: False)
- can_access_orders: bool (default: False)
- can_access_users: bool (default: False)
- can_access_configuration: bool (default: False)
- can_access_reports: bool (default: False)
- created_at: datetime
- updated_at: datetime
```

**Relación:** One-to-One con `User`

### Endpoints

**Base URL:** `/api/permissions`

#### GET `/api/permissions/{user_id}`
Obtener permisos de un usuario

**Permisos:** Solo Admin
**Response:**
```json
{
  "id": 1,
  "user_id": 5,
  "can_access_dashboard": true,
  "can_access_inventory": true,
  "can_access_products": false,
  ...
}
```

#### PUT `/api/permissions/{user_id}`
Actualizar permisos de un usuario

**Permisos:** Solo Admin
**Request Body:**
```json
{
  "can_access_dashboard": true,
  "can_access_inventory": true,
  "can_access_products": true,
  ...
}
```

**Response:** Objeto de permisos actualizado

---

## 🎨 Frontend - Implementación

### Componente: `UserPermissionsModalComponent`

**Ubicación:** `frontend/src/app/shared/components/user-permissions-modal/`

**Características:**
- ✅ Modal elegante con diseño moderno
- ✅ Grid responsive de tarjetas de permisos
- ✅ Checkboxes visuales (estilo switch/card)
- ✅ Iconos descriptivos para cada módulo
- ✅ Guardado automático con feedback visual
- ✅ Totalmente responsive (mobile-friendly)

**Inputs:**
```typescript
@Input() user: User | null = null;        // Usuario a gestionar
@Input() isOpen = false;                  // Estado del modal
```

**Outputs:**
```typescript
@Output() closeModal = new EventEmitter<void>();
@Output() permissionsSaved = new EventEmitter<void>();
```

### Servicio: `PermissionService`

**Ubicación:** `frontend/src/app/core/services/permission.service.ts`

**Métodos:**
```typescript
getUserPermissions(userId: number): Observable<UserPermission>
updateUserPermissions(userId: number, permissions: PermissionUpdate): Observable<UserPermission>
```

### Modelo: `permission.model.ts`

**Ubicación:** `frontend/src/app/core/models/permission.model.ts`

**Interfaces:**
- `UserPermission` - Permisos completos del usuario
- `PermissionUpdate` - Para actualizaciones parciales
- `PermissionModule` - Metadata de cada módulo

**Constante:**
- `PERMISSION_MODULES` - Array con información de cada módulo (label, descripción, icono)

---

## 🎯 Cómo Usar

### En el Frontend (Componente de Usuarios)

1. **Botón de Candado:**
   - Aparece en cada tarjeta de usuario
   - Solo visible para administradores
   - Al hacer clic, abre el modal de permisos

```html
<button
  (click)="openPermissionsModal(user)"
  class="btn-info text-sm py-2 px-3"
  title="Gestionar permisos"
>
  🔒
</button>
```

2. **Modal de Permisos:**
   - Se abre automáticamente al hacer clic en el candado
   - Muestra todos los módulos disponibles
   - Permite marcar/desmarcar permisos
   - Guarda cambios con confirmación visual

### En el Código TypeScript

```typescript
// Abrir modal de permisos
openPermissionsModal(user: User): void {
  this.selectedUserForPermissions = user;
  this.showPermissionsModal = true;
}

// Cerrar modal
closePermissionsModal(): void {
  this.showPermissionsModal = false;
  this.selectedUserForPermissions = null;
}

// Callback cuando se guardan permisos
onPermissionsSaved(): void {
  this.notificationService.success('Los permisos han sido actualizados');
}
```

---

## 🔄 Flujo de Uso

1. **Administrador accede a Usuarios**
   - Ve lista de todos los usuarios
   - Cada tarjeta de usuario muestra un candado 🔒

2. **Click en el candado**
   - Se abre modal de permisos
   - Carga automáticamente los permisos actuales del usuario
   - Si no tiene permisos, crea unos por defecto

3. **Configurar permisos**
   - Click en las tarjetas para activar/desactivar módulos
   - Las tarjetas activas se destacan visualmente
   - Cada módulo muestra icono, nombre y descripción

4. **Guardar**
   - Click en "Guardar Permisos"
   - Se actualizan en el backend
   - Notificación de éxito
   - Modal se cierra automáticamente

---

## 🎨 Diseño del Modal

### Estructura Visual

```
┌─────────────────────────────────────────┐
│ 🔒 Permisos de Acceso                  │
│    Juan Pérez (@juan.perez)            │
├─────────────────────────────────────────┤
│                                         │
│ [✓] 📊 Dashboard                       │
│     Acceso al panel principal          │
│                                         │
│ [✓] 📦 Inventario                      │
│     Gestión de inventario              │
│                                         │
│ [ ] 🏷️ Productos                       │
│     Gestión de productos               │
│                                         │
│ [✓] 📋 Órdenes                         │
│     Gestión de órdenes                 │
│                                         │
│ ...                                     │
├─────────────────────────────────────────┤
│           [Cancelar] [💾 Guardar]       │
└─────────────────────────────────────────┘
```

### Estados Visuales

- **Activo:** Borde azul, fondo azul claro
- **Inactivo:** Borde gris, fondo blanco
- **Hover:** Sombra y resaltado sutil

---

## 🛡️ Seguridad

### Restricciones:

1. **Solo administradores** pueden gestionar permisos
2. Los permisos se validan en el **backend**
3. Relación **CASCADE** - Si se elimina un usuario, se eliminan sus permisos
4. Filtros por **business_id** - Solo usuarios del mismo negocio
5. Soft delete compatible - No afecta a usuarios eliminados

### Próximos Pasos (Opcional):

- [ ] Implementar validación de permisos en guards del frontend
- [ ] Middleware de permisos en el backend
- [ ] Ocultar menús basados en permisos
- [ ] Logs de cambios de permisos

---

## 📊 Tabla de Base de Datos

### user_permissions

```sql
CREATE TABLE user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    can_access_dashboard BOOLEAN DEFAULT true,
    can_access_inventory BOOLEAN DEFAULT false,
    can_access_products BOOLEAN DEFAULT false,
    can_access_menu BOOLEAN DEFAULT false,
    can_access_tables BOOLEAN DEFAULT false,
    can_access_orders BOOLEAN DEFAULT false,
    can_access_users BOOLEAN DEFAULT false,
    can_access_configuration BOOLEAN DEFAULT false,
    can_access_reports BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id)
);
```

**Migración ejecutada:** ✅

---

## 💡 Casos de Uso

### Ejemplo 1: Mesero Básico
```
✅ Dashboard    - Ver estadísticas básicas
✅ Órdenes      - Crear y gestionar órdenes
✅ Mesas        - Ver estado de mesas
❌ Inventario   - No tiene acceso
❌ Configuración - No tiene acceso
❌ Usuarios     - No tiene acceso
```

### Ejemplo 2: Cajero
```
✅ Dashboard    - Ver estadísticas
✅ Órdenes      - Gestionar pagos
❌ Inventario   - No tiene acceso
❌ Productos    - No tiene acceso
❌ Usuarios     - No tiene acceso
```

### Ejemplo 3: Gerente
```
✅ Dashboard     - Acceso completo
✅ Inventario    - Gestión completa
✅ Productos     - Gestión completa
✅ Menú          - Gestión completa
✅ Órdenes       - Supervisión
✅ Usuarios      - Gestión limitada
❌ Configuración - Solo Admin
```

---

## 🔄 Migración

Si ya tienes usuarios existentes:

1. **Ejecutar script de migración:**
```bash
cd backend
.venv/Scripts/python.exe create_permissions_table.py
```

2. **Reiniciar servidor backend**

3. Los permisos se crean automáticamente cuando:
   - Un admin accede al modal de permisos de un usuario
   - Se consultan por primera vez

4. **Por defecto**, todos los usuarios nuevos tendrán:
   - ✅ Acceso al Dashboard
   - ❌ Resto de módulos desactivados

---

## 🎉 Beneficios

✅ **Control granular** - Permisos específicos por módulo  
✅ **Flexibilidad** - Adapta el sistema a diferentes roles  
✅ **Seguridad** - Solo admin puede modificar permisos  
✅ **UX Excelente** - Interfaz intuitiva y visual  
✅ **Auditoría** - Timestamps de creación y actualización  
✅ **Escalable** - Fácil agregar nuevos módulos  
✅ **Reutilizable** - Componente standalone  

---

**Implementado:** ✅  
**Fecha:** ${new Date().toLocaleDateString('es-ES')}  
**Versión:** 2.1.0

