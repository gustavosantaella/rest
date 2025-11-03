# Implementación de Soft Delete y Sistema de Notificaciones

## Resumen de Cambios

### Backend - Soft Delete Implementado

Se ha implementado **soft delete** (eliminación suave) en todos los modelos principales del sistema. Esto significa que cuando se "elimina" un registro, en realidad solo se marca con una fecha de eliminación (`deleted_at`), permitiendo recuperación futura si es necesario.

#### Modelos Actualizados:
- ✅ **User** - Usuarios del sistema
- ✅ **Product** - Productos del inventario
- ✅ **Category** - Categorías de productos
- ✅ **MenuItem** - Items del menú
- ✅ **MenuCategory** - Categorías del menú
- ✅ **Table** - Mesas del restaurante
- ✅ **PaymentMethod** - Métodos de pago
- ✅ **OrderItem** - Items de órdenes

#### Routers Actualizados con Soft Delete:
- ✅ `users.py` - Gestión de usuarios
- ✅ `products.py` - Gestión de productos
- ✅ `menu.py` - Gestión del menú
- ✅ `tables.py` - Gestión de mesas
- ✅ `payment_methods.py` - Gestión de métodos de pago

**Nota**: Las órdenes (`Order`) no tienen soft delete por su naturaleza histórica y contable.

### Endpoint de Eliminación Permanente

Se agregó un endpoint especial en `profile.py` para **eliminación permanente** del negocio:

```
DELETE /api/dashboard/profile/delete-account-permanently
```

**Características**:
- Solo accesible para administradores
- Requiere confirmación de contraseña
- Elimina PERMANENTEMENTE:
  - Todos los usuarios del negocio
  - Todos los productos y categorías
  - Todas las órdenes e items
  - Todos los métodos de pago
  - Todo el menú y categorías
  - Todas las mesas
  - Toda la configuración del negocio
  - Todos los socios

⚠️ **ADVERTENCIA**: Esta acción es **IRREVERSIBLE**

### Organización de Rutas API

Las rutas ahora están organizadas de la siguiente manera:

#### Rutas Públicas (`/api`):
- `/api/auth/*` - Autenticación y registro
- `/api/public/*` - Catálogo público

#### Rutas del Dashboard (`/api/dashboard`):
- `/api/dashboard/users/*` - Gestión de usuarios
- `/api/dashboard/products/*` - Gestión de productos
- `/api/dashboard/tables/*` - Gestión de mesas
- `/api/dashboard/orders/*` - Gestión de órdenes
- `/api/dashboard/menu/*` - Gestión del menú
- `/api/dashboard/configuration/*` - Configuración del negocio
- `/api/dashboard/profile/*` - Perfil del usuario
- `/api/dashboard/payment-methods/*` - Métodos de pago
- `/api/dashboard/upload/*` - Subida de archivos

### Frontend - Sistema de Notificaciones

#### 1. Componente Toast Reutilizable

Se creó `ToastNotificationComponent` con las siguientes características:

- **4 tipos de notificaciones**:
  - ✅ Success (verde)
  - ❌ Error (rojo)
  - ⚠️ Warning (amarillo)
  - ℹ️ Info (azul)

- **Características**:
  - Animaciones suaves de entrada/salida
  - Auto-dismiss configurable
  - Click para cerrar
  - Diseño responsive
  - Posición fija superior derecha
  - Múltiples toasts simultáneos

**Ubicación**: `frontend/src/app/shared/components/toast-notification/`

#### 2. Servicio de Notificaciones

`NotificationService` proporciona métodos simples:

```typescript
// Uso básico
notificationService.success('Operación exitosa');
notificationService.error('Error al procesar');
notificationService.warning('Advertencia importante');
notificationService.info('Información relevante');

// Con duración personalizada
notificationService.success('Guardado', 3000); // 3 segundos
```

**Ubicación**: `frontend/src/app/core/services/notification.service.ts`

#### 3. Sistema de Confirmación Reutilizable

Se implementó un sistema de confirmación con modal para acciones críticas.

##### Componente: `ConfirmDialogComponent`
- Modal con overlay
- Diseño atractivo con iconos
- Tres tipos: danger, warning, info
- Animaciones de entrada/salida
- Responsive

**Ubicación**: `frontend/src/app/shared/components/confirm-dialog/`

##### Servicio: `ConfirmService`

```typescript
// Confirmación genérica
confirmService.confirm({
  title: '¿Confirmar acción?',
  message: 'Descripción de lo que va a pasar',
  confirmText: 'Sí, continuar',
  cancelText: 'No, cancelar',
  type: 'warning'
}).subscribe(confirmed => {
  if (confirmed) {
    // Usuario confirmó
  }
});

// Método helper para eliminación
confirmService.confirmDelete('Usuario Juan Pérez').subscribe(confirmed => {
  if (confirmed) {
    // Proceder con eliminación
  }
});

// Método helper para cambios
confirmService.confirmChanges('¿Guardar cambios?').subscribe(confirmed => {
  if (confirmed) {
    // Guardar cambios
  }
});
```

**Ubicación**: `frontend/src/app/core/services/confirm.service.ts`

### Componentes Actualizados

#### ✅ UsersComponent
- Reemplazados `alert()` por `notificationService`
- Implementada confirmación antes de eliminar
- Mensajes de éxito/error para crear/editar/eliminar

#### ✅ ProfileComponent
- Reemplazados `alert()` por `notificationService`
- Mensajes de éxito/error para actualizar perfil
- Notificación al cambiar contraseña

#### 🔄 Pendientes de actualizar:
- OrdersComponent (~10 alerts)
- ConfigurationComponent (~12 alerts)
- InventoryComponent (si tiene alerts)
- MenuComponent (si tiene alerts)
- TablesComponent (si tiene alerts)

## Cómo Usar

### Backend - Consultas con Soft Delete

Todos los endpoints de listado ahora filtran automáticamente los registros eliminados:

```python
# Ejemplo en cualquier router
users = db.query(User).filter(
    User.deleted_at.is_(None)  # Solo usuarios no eliminados
).all()
```

### Frontend - Notificaciones

1. **Inyectar el servicio**:
```typescript
private notificationService = inject(NotificationService);
```

2. **Usar en operaciones**:
```typescript
this.service.save(data).subscribe({
  next: () => {
    this.notificationService.success('Guardado exitosamente');
  },
  error: (err) => {
    this.notificationService.error('Error: ' + err.error?.detail);
  }
});
```

### Frontend - Confirmaciones

1. **Inyectar el servicio**:
```typescript
private confirmService = inject(ConfirmService);
```

2. **Confirmar antes de eliminar**:
```typescript
deleteItem(item: any) {
  this.confirmService.confirmDelete(item.name).subscribe(confirmed => {
    if (confirmed) {
      this.service.delete(item.id).subscribe({
        next: () => {
          this.notificationService.success('Eliminado exitosamente');
          this.loadItems();
        },
        error: (err) => {
          this.notificationService.error('Error al eliminar');
        }
      });
    }
  });
}
```

## Beneficios

### Soft Delete:
✅ Recuperación de datos accidentalmente eliminados
✅ Auditoría y trazabilidad completa
✅ Cumplimiento con normativas de datos
✅ Sin pérdida de integridad referencial
✅ Historial completo de cambios

### Sistema de Notificaciones:
✅ Mejor UX con feedback visual
✅ Consistencia en toda la aplicación
✅ Fácil de usar y mantener
✅ Diseño moderno y profesional
✅ Totalmente reutilizable

### Sistema de Confirmación:
✅ Previene eliminaciones accidentales
✅ Interfaz clara y profesional
✅ Totalmente customizable
✅ Reutilizable en toda la app
✅ Mejora significativa en UX

## Migración de Datos

⚠️ **IMPORTANTE**: Si ya tienes una base de datos existente:

1. Las columnas `deleted_at` se crearán automáticamente al reiniciar el backend
2. Todos los registros existentes tendrán `deleted_at = NULL` (no eliminados)
3. No se perderán datos existentes
4. El sistema es retrocompatible

## Próximos Pasos

1. ✅ Completar la actualización de todos los componentes frontend
2. ✅ Agregar tests para el soft delete
3. ✅ Documentar el endpoint de eliminación permanente en Swagger
4. ✅ Crear un panel de administración para ver/recuperar registros eliminados (opcional)

---

**Fecha de implementación**: ${new Date().toLocaleDateString('es-ES')}
**Versión**: 2.0.0

