# 👥 Sistema de Roles y Permisos

## 📋 Roles Disponibles

El sistema cuenta con **5 roles** diferentes, cada uno con permisos específicos:

---

## 1. 👑 **ADMIN** (Administrador)

### Permisos:
- ✅ **Acceso total** al sistema
- ✅ Gestión completa de usuarios
- ✅ Gestión de inventario
- ✅ Gestión del menú
- ✅ Gestión de mesas
- ✅ Gestión de órdenes
- ✅ Ver todas las estadísticas
- ✅ Configuración del sistema

### Caso de Uso:
Dueño o gerente general del negocio.

### Badge Color:
🔴 Rojo

---

## 2. 💼 **MANAGER** (Gerente)

### Permisos:
- ✅ Gestión de inventario (crear, editar, eliminar)
- ✅ Gestión del menú (crear, editar, eliminar)
- ✅ Gestión de mesas
- ✅ Gestión de usuarios (Waiter, Cashier, Chef)
- ✅ Ver órdenes
- ✅ Ver reportes
- ❌ No puede gestionar otros Admins o Managers

### Caso de Uso:
Gerente de operaciones, supervisor de turno.

### Badge Color:
🟡 Amarillo

---

## 3. 🍽️ **WAITER** (Mesero)

### Permisos:
- ✅ Crear órdenes
- ✅ Actualizar órdenes
- ✅ Gestionar mesas (cambiar estados)
- ✅ Ver inventario (solo lectura)
- ✅ Ver menú (solo lectura)
- ❌ No puede ver usuarios
- ❌ No puede gestionar inventario
- ❌ No puede procesar pagos

### Caso de Uso:
Personal de servicio que toma órdenes.

### Badge Color:
🔵 Azul

---

## 4. 💰 **CASHIER** (Cajero)

### Permisos:
- ✅ Ver órdenes
- ✅ Procesar pagos
- ✅ Marcar órdenes como pagadas
- ✅ Aplicar descuentos
- ✅ Ver métodos de pago
- ❌ No puede crear órdenes
- ❌ No puede gestionar inventario
- ❌ No puede gestionar usuarios

### Caso de Uso:
Personal de caja que cobra las cuentas.

### Badge Color:
🟢 Verde

---

## 5. 👨‍🍳 **CHEF** (Cocinero) - ¡NUEVO!

### Permisos:
- ✅ **Ver todas las órdenes**
- ✅ **Actualizar estado de órdenes**:
  - Pendiente → En Progreso
  - En Progreso → Completada
- ✅ Ver detalles de platillos
- ✅ Ver ingredientes necesarios
- ❌ No puede crear/eliminar órdenes
- ❌ No puede procesar pagos
- ❌ No puede gestionar inventario
- ❌ No puede gestionar usuarios

### Caso de Uso:
Personal de cocina que prepara los platillos.

### Badge Color:
🟠 Naranja

---

## 📊 Matriz de Permisos

| Funcionalidad | Admin | Manager | Waiter | Cashier | Chef |
|---------------|-------|---------|--------|---------|------|
| **Usuarios** |
| Ver usuarios | ✅ | ✅ | ❌ | ❌ | ❌ |
| Crear usuarios | ✅ | ✅* | ❌ | ❌ | ❌ |
| Editar usuarios | ✅ | ✅* | ❌ | ❌ | ❌ |
| Eliminar usuarios | ✅ | ✅* | ❌ | ❌ | ❌ |
| **Inventario** |
| Ver productos | ✅ | ✅ | ✅ | ✅ | ❌ |
| Crear productos | ✅ | ✅ | ❌ | ❌ | ❌ |
| Editar productos | ✅ | ✅ | ❌ | ❌ | ❌ |
| Eliminar productos | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Menú** |
| Ver menú | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crear platillos | ✅ | ✅ | ❌ | ❌ | ❌ |
| Editar platillos | ✅ | ✅ | ❌ | ❌ | ❌ |
| Eliminar platillos | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Mesas** |
| Ver mesas | ✅ | ✅ | ✅ | ✅ | ❌ |
| Crear mesas | ✅ | ✅ | ❌ | ❌ | ❌ |
| Cambiar estado mesas | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Órdenes** |
| Ver órdenes | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crear órdenes | ✅ | ✅ | ✅ | ❌ | ❌ |
| Actualizar estado | ✅ | ✅ | ✅ | ✅ | ✅ |
| Procesar pago | ✅ | ✅ | ❌ | ✅ | ❌ |
| Eliminar órdenes | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Dashboard** |
| Ver estadísticas | ✅ | ✅ | ✅ | ✅ | ✅ |

\* Manager solo puede gestionar usuarios con roles inferiores (Waiter, Cashier, Chef)

---

## 🔄 Flujo de Trabajo por Rol

### Flujo del Mesero:
```
1. Cliente llega → Asigna mesa
2. Toma orden → Selecciona platillos del menú
3. Envía orden a cocina
4. Actualiza estado de mesa
```

### Flujo del Cocinero:
```
1. Ve nuevas órdenes (Estado: Pendiente)
2. Comienza a preparar → Cambia a "En Progreso"
3. Termina de preparar → Cambia a "Completada"
4. Mesero recoge y sirve
```

### Flujo del Cajero:
```
1. Cliente pide cuenta
2. Ve orden completada
3. Procesa pago (Efectivo/Tarjeta/etc.)
4. Marca como "Pagada"
5. Mesa queda disponible
```

---

## 🎯 Recomendaciones de Uso

### Restaurante Pequeño:
```
1 Admin (Dueño)
1 Manager (Gerente de turno)
2-3 Waiters (Meseros)
1 Chef (Cocinero)
1 Cashier (Cajero)
```

### Restaurante Mediano:
```
1 Admin (Dueño)
2 Managers (Turno mañana/noche)
5-8 Waiters (Meseros)
2-3 Chefs (Cocineros)
2 Cashiers (Cajeros)
```

### Restaurante Grande:
```
1 Admin (Dueño)
3-4 Managers (Por área/turno)
10+ Waiters (Meseros)
5+ Chefs (Cocina)
3-4 Cashiers (Cajas)
```

---

## 🔐 Seguridad

### Jerarquía de Roles:
```
Admin (máximo)
  └── Manager
      └── Waiter
      └── Cashier
      └── Chef (mismo nivel)
```

### Reglas:
1. Solo Admin puede crear otros Admins
2. Manager no puede editar a otros Managers
3. Nadie puede eliminar su propia cuenta
4. Usuarios pueden cambiar su propia contraseña

---

## 💡 Tips de Configuración

### Primer Usuario:
```
Rol: Admin
Usuario: admin
Password: 123456.Ab!
```

### Crear Personal:
```
1. Login como Admin
2. Ve a Usuarios
3. Click "+ Nuevo Usuario"
4. Selecciona el rol apropiado
5. Asigna credenciales
6. Entregar credenciales al empleado
```

### Rotación de Personal:
```
Empleado sale → Desactivar usuario (no eliminar)
Nuevo empleado → Crear nuevo usuario
Empleado temporal → Crear y desactivar después
```

---

## 🎨 Personalización de Permisos

Si necesitas permisos más específicos en el futuro:

### Backend (`utils/dependencies.py`):
```python
async def get_current_active_inventory_manager(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Sin permisos")
    return current_user
```

### Aplicar en Router:
```python
@router.post("/products/")
def create_product(
    ...,
    current_user: User = Depends(get_current_active_inventory_manager)
):
```

---

## 📱 Interfaz por Rol

### Lo que ve cada rol en el Sidebar:

#### Admin / Manager:
```
Dashboard
Inventario
Menú
Mesas
Órdenes
Usuarios
```

#### Waiter:
```
Dashboard
Inventario (solo lectura)
Menú (solo lectura)
Mesas
Órdenes
```

#### Cashier:
```
Dashboard
Órdenes
```

#### Chef:
```
Dashboard
Menú (solo lectura)
Órdenes (solo lectura + actualizar estado)
```

---

## 🔄 Cambios de Rol

### Promoción:
```
Waiter destacado → Manager
Chef experimentado → Manager
```

### Degradación:
```
Manager que ya no supervisa → Waiter
```

### Cambio:
```
1. Login como Admin/Manager
2. Ve a Usuarios
3. Edita el usuario
4. Cambia el rol
5. Guardar
```

---

**Sistema de 5 roles completamente implementado** ✅

- Admin
- Manager  
- Waiter
- Cashier
- **Chef** (Nuevo)

