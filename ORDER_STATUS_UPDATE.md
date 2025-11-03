# ✅ Estados de Orden Actualizados

## 🔄 Cambios Realizados

### Estados Simplificados

**ANTES:**
```
- PENDING (Pendiente)
- IN_PROGRESS (En Progreso)
- COMPLETED (Completada)
- CANCELLED (Cancelada)
- PAID (Pagada) ← Redundante
```

**AHORA:**
```
- PENDING (Pendiente) 🟡
- PREPARING (Preparando) 🔵
- COMPLETED (Completada) 🟢
- CANCELLED (Cancelada) 🔴
```

### ¿Por qué eliminar PAID?

El estado `PAID` es redundante porque ahora tenemos `payment_status`:

**Estados de Orden (status):**
- Describe el **progreso de preparación**
- PENDING → PREPARING → COMPLETED

**Estados de Pago (payment_status):**
- Describe el **estado del pago**
- pending → partial → paid

**Ventajas:**
- ✅ Separación clara de responsabilidades
- ✅ Una orden puede estar "Completada" pero "Pendiente de pago"
- ✅ Una orden puede estar "Preparando" pero "Pagada"
- ✅ Más flexible y realista

---

## 🎯 Flujo Actualizado

### Flujo Típico de Restaurante

```
1. Mesero toma pedido
   → status: PENDING
   → payment_status: pending
   
2. Mesero envía a cocina
   → status: PREPARING
   → payment_status: pending
   
3. Cocina termina
   → status: COMPLETED
   → payment_status: pending
   
4. Cliente paga
   → status: COMPLETED
   → payment_status: paid
   
5. Mesa liberada ✅
```

### Flujo Para Llevar (Pago Adelantado)

```
1. Cliente pide y paga
   → status: PENDING
   → payment_status: paid
   
2. Cocina prepara
   → status: PREPARING
   → payment_status: paid
   
3. Orden lista
   → status: COMPLETED
   → payment_status: paid
   
4. Cliente retira ✅
```

---

## 🎨 Badges Visuales

| Estado | Badge | Color | Cuándo |
|--------|-------|-------|---------|
| **Pendiente** | `[Pendiente]` | 🟡 Amarillo | Orden recién creada |
| **Preparando** | `[Preparando]` | 🔵 Azul | En cocina |
| **Completada** | `[Completada]` | 🟢 Verde | Lista para servir |
| **Cancelada** | `[Cancelada]` | 🔴 Rojo | Orden cancelada |

---

## 💡 Combinaciones Posibles

### Status + Payment Status

| Status | Payment Status | Significado | Ejemplo |
|--------|---------------|-------------|---------|
| Pendiente | Pending | Recién ordenada, sin pago | Mesa acaba de pedir |
| Pendiente | Paid | Ordenada y pagada, esperando cocina | Para llevar pagado |
| Preparando | Pending | Cocinando, sin pago | Orden en cocina |
| Preparando | Paid | Cocinando, ya pagada | Para llevar en cocina |
| Completada | Pending | Lista, esperando pago | Mesa pide cuenta |
| Completada | Paid | Lista y pagada | Listo para entregar |
| Completada | Partial | Lista, pago parcial | Falta saldo |
| Cancelada | * | Cancelada (cualquier estado pago) | Cancelación |

---

## 🔧 Reglas de Edición

### Se puede editar:
- ✅ Status: **PENDING** (Pendiente)
- ✅ Status: **PREPARING** (Preparando)

### NO se puede editar:
- ❌ Status: **COMPLETED** (Ya está lista)
- ❌ Status: **CANCELLED** (Cancelada)

**Razón:** Una vez que la cocina termina (COMPLETED), no tiene sentido agregar más items porque ya está servida/lista para entregar.

---

## 🎯 Botones según Estado

### PENDING (Pendiente):
```
✏️ Editar - Sí
💲 Pagar - Sí (si no está paid)
```

### PREPARING (Preparando):
```
✏️ Editar - Sí (por si el cliente cambia de opinión)
💲 Pagar - Sí (puede pagar mientras cocina)
```

### COMPLETED (Completada):
```
✏️ Editar - NO (ya está lista)
💲 Pagar - Sí (si no está paid)
```

### CANCELLED (Cancelada):
```
✏️ Editar - NO
💲 Pagar - NO
```

---

## 📋 Changelog

### Backend
- ✅ `OrderStatus.PAID` eliminado
- ✅ `OrderStatus.IN_PROGRESS` → `OrderStatus.PREPARING`
- ✅ Validación de edición actualizada
- ✅ Comentarios en el código

### Frontend
- ✅ Enum actualizado
- ✅ Labels en español actualizados
- ✅ Badge classes actualizados
- ✅ Lógica `canEditOrder()` actualizada
- ✅ Comentarios explicativos

---

## 🎊 Estados Finales

```
┌─────────────────────────────────────────────┐
│ Estados de Orden (4):                       │
│ ─────────────────────────────────────────── │
│ 🟡 PENDING    - Pendiente                   │
│ 🔵 PREPARING  - Preparando (en cocina)      │
│ 🟢 COMPLETED  - Completada (lista)          │
│ 🔴 CANCELLED  - Cancelada                   │
├─────────────────────────────────────────────┤
│ Estados de Pago (3):                        │
│ ─────────────────────────────────────────── │
│ 🟡 pending  - Sin pago                      │
│ 🔵 partial  - Pago parcial                  │
│ 🟢 paid     - Completamente pagado          │
└─────────────────────────────────────────────┘

Independientes entre sí ✅
Más flexibles ✅
Más claros ✅
```

---

**¡Estados actualizados y simplificados!** 🎉

Ahora el sistema es más claro y refleja mejor el flujo real de un restaurante.

