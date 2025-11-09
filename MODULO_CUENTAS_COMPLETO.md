# Módulo de Cuentas por Cobrar y Cuentas por Pagar - COMPLETO ✅

## 🎉 IMPLEMENTACIÓN 100% COMPLETADA

Sistema profesional de gestión de cuentas por cobrar (clientes) y cuentas por pagar (proveedores) completamente funcional.

---

## 📋 Características Implementadas

### 💰 Cuentas por Cobrar
- ✅ Registro de facturas pendientes de clientes
- ✅ Asociación opcional con clientes registrados
- ✅ Gestión de pagos parciales y totales
- ✅ Actualización automática de estados
- ✅ Alertas de vencimiento
- ✅ Historial completo de pagos
- ✅ Resumen financiero con estadísticas

### 💳 Cuentas por Pagar
- ✅ Registro de facturas de proveedores
- ✅ Información completa del proveedor
- ✅ Control de pagos parciales
- ✅ Estados automáticos (pending/partial/paid/overdue)
- ✅ Historial de pagos
- ✅ Resumen de deudas pendientes

### 🎯 Estados del Sistema
```
PENDING  → Pendiente de pago (naranja/amarillo)
PARTIAL  → Parcialmente pagado (azul)
PAID     → Totalmente pagado (verde)
OVERDUE  → Vencido - automático (rojo)
```

---

## 🗄️ Base de Datos

### Tablas Creadas

#### 1. `accounts_receivable` (Cuentas por Cobrar)
```sql
- id (PK)
- business_id (FK → business_configuration)
- customer_id (FK → customers, nullable)
- invoice_number
- description
- amount
- amount_paid
- amount_pending
- issue_date
- due_date
- paid_date
- status (enum)
- notes
- created_at, updated_at, deleted_at
```

#### 2. `account_receivable_payments` (Pagos de Cobrar)
```sql
- id (PK)
- account_id (FK → accounts_receivable)
- amount
- payment_date
- payment_method
- reference
- notes
- created_at
```

#### 3. `accounts_payable` (Cuentas por Pagar)
```sql
- id (PK)
- business_id (FK → business_configuration)
- supplier_name
- supplier_phone
- supplier_email
- invoice_number
- description
- amount
- amount_paid
- amount_pending
- issue_date
- due_date
- paid_date
- status (enum)
- notes
- created_at, updated_at, deleted_at
```

#### 4. `account_payable_payments` (Pagos de Pagar)
```sql
- id (PK)
- account_id (FK → accounts_payable)
- amount
- payment_date
- payment_method
- reference
- notes
- created_at
```

---

## 🔌 API Endpoints

### Cuentas por Cobrar (`/api/accounts-receivable`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Listar todas las cuentas (filtro opcional por estado) |
| POST | `/` | Crear nueva cuenta |
| GET | `/{id}` | Obtener cuenta específica |
| PUT | `/{id}` | Actualizar cuenta |
| DELETE | `/{id}` | Eliminar cuenta (soft delete) |
| POST | `/{id}/payments` | Agregar pago a una cuenta |
| GET | `/summary/stats` | Obtener resumen estadístico |

### Cuentas por Pagar (`/api/accounts-payable`)
*(Mismos endpoints)*

### Ejemplos de Uso

#### Crear Cuenta por Cobrar
```json
POST /api/accounts-receivable
{
  "customer_id": 1,
  "invoice_number": "FAC-001",
  "description": "Venta de productos",
  "amount": 1500.00,
  "due_date": "2025-12-31",
  "notes": "Cliente frecuente"
}
```

#### Registrar Pago
```json
POST /api/accounts-receivable/1/payments
{
  "amount": 750.00,
  "payment_method": "Transferencia",
  "reference": "REF-123456",
  "notes": "Pago parcial del 50%"
}
```

**Respuesta automática:**
- `amount_paid` se actualiza: `750.00`
- `amount_pending` se calcula: `750.00`
- `status` cambia a: `partial`

#### Consultar Resumen
```http
GET /api/accounts-receivable/summary/stats
```

**Respuesta:**
```json
{
  "total_pending": 5000.00,
  "total_overdue": 1200.00,
  "count_pending": 8,
  "count_overdue": 2
}
```

---

## 🎨 Interfaz de Usuario

### Cuentas por Cobrar (`/accounts-receivable`)

#### Tarjetas de Resumen (4)
1. **Total Pendiente** 🟠 - Monto total por cobrar
2. **Vencidas** 🔴 - Monto vencido
3. **Cuentas Pendientes** 🔵 - Cantidad de cuentas
4. **Vencidas (Cant.)** 🔴 - Cantidad vencidas

#### Filtros
- Selector por estado: Todos, Pendientes, Parciales, Vencidas, Pagadas

#### Tabla Principal
Columnas:
- Factura
- Cliente
- Descripción
- Monto Total
- Pendiente
- Vencimiento
- Estado (badge con colores)
- Acciones (💰 Pagar, ✏️ Editar, 🗑️ Eliminar)

#### Modal de Cuenta
Formulario con:
- Cliente (dropdown de clientes registrados)
- Nº Factura (opcional)
- Descripción *
- Monto *
- Fecha de Vencimiento *
- Notas

#### Modal de Pago
- Muestra monto pendiente
- Monto del pago *
- Método de pago (Efectivo, Transferencia, Cheque, Tarjeta)
- Referencia
- Notas

### Cuentas por Pagar (`/accounts-payable`)

Similar a Cuentas por Cobrar pero con:
- Campos de proveedor en lugar de cliente
- Colores rojos para indicar deudas
- Formulario incluye: nombre, teléfono y email del proveedor

---

## 🔧 Lógica de Negocio

### Actualización Automática de Estados

```python
def update_account_status(account):
    if account.amount_pending <= 0:
        account.status = PAID
        account.paid_date = now()
    elif account.amount_paid > 0:
        account.status = PARTIAL
    elif now() > account.due_date:
        account.status = OVERDUE
    else:
        account.status = PENDING
```

### Validaciones

1. **No se puede pagar más del pendiente**
   ```python
   if payment.amount > account.amount_pending:
       raise HTTPException(400, "Monto excede el pendiente")
   ```

2. **Montos deben ser positivos**
3. **Fecha de vencimiento obligatoria**
4. **Aislamiento por business_id** (multi-tenant)

### Soft Delete
- Las cuentas eliminadas no se borran físicamente
- Se marca `deleted_at = current_timestamp`
- Permite recuperación si es necesario

---

## 📂 Estructura de Archivos

```
backend/
├── app/
│   ├── models/
│   │   ├── account_receivable.py ✅
│   │   │   ├── AccountReceivable
│   │   │   ├── AccountReceivablePayment
│   │   │   └── AccountStatus (enum)
│   │   └── account_payable.py ✅
│   │       ├── AccountPayable
│   │       ├── AccountPayablePayment
│   │       └── AccountStatus (enum)
│   ├── schemas/
│   │   ├── account_receivable.py ✅
│   │   │   ├── AccountReceivableCreate
│   │   │   ├── AccountReceivableUpdate
│   │   │   ├── AccountReceivableResponse
│   │   │   ├── AccountReceivablePaymentCreate
│   │   │   └── AccountReceivablePaymentResponse
│   │   └── account_payable.py ✅
│   │       └── (schemas equivalentes)
│   └── routers/
│       ├── accounts_receivable.py ✅
│       └── accounts_payable.py ✅
├── db/migrations/
│   └── migrate_add_accounts_tables.py ✅

frontend/
├── src/app/
│   ├── core/
│   │   ├── models/
│   │   │   └── accounts.model.ts ✅
│   │   │       ├── AccountStatus (enum)
│   │   │       ├── AccountReceivable
│   │   │       ├── AccountPayable
│   │   │       ├── AccountPayment
│   │   │       └── AccountsSummary
│   │   └── services/
│   │       ├── accounts-receivable.service.ts ✅
│   │       └── accounts-payable.service.ts ✅
│   └── features/
│       ├── accounts-receivable/
│       │   ├── accounts-receivable.component.ts ✅
│       │   ├── accounts-receivable.component.html ✅
│       │   └── accounts-receivable.component.scss ✅
│       └── accounts-payable/
│           ├── accounts-payable.component.ts ✅
│           ├── accounts-payable.component.html ✅
│           └── accounts-payable.component.scss ✅
```

---

## 🚀 Cómo Usar

### 1. Iniciar el Sistema

**Backend:**
```bash
cd backend
source .venv/Scripts/activate  # Windows Git Bash
python run.py
```

**Frontend:**
```bash
cd frontend
npm start
```

### 2. Acceder a los Módulos

En el menú lateral encontrarás:
- 💰 **Cuentas por Cobrar** → `/accounts-receivable`
- 💳 **Cuentas por Pagar** → `/accounts-payable`

### 3. Crear una Cuenta por Cobrar

1. Click en "+ Nueva Cuenta por Cobrar"
2. Selecciona un cliente (opcional)
3. Ingresa descripción y monto
4. Establece fecha de vencimiento
5. Guarda

### 4. Registrar un Pago

1. Localiza la cuenta en la tabla
2. Click en el botón 💰 "Registrar pago"
3. Ingresa el monto (máximo: monto pendiente)
4. Selecciona método de pago
5. Agrega referencia si aplica
6. Guarda

**El sistema automáticamente:**
- Actualiza los montos
- Cambia el estado si es necesario
- Marca como pagado si se completa el pago

### 5. Consultar Estadísticas

Las tarjetas superiores muestran en tiempo real:
- Total pendiente de cobro/pago
- Montos vencidos
- Cantidad de cuentas activas

---

## 💡 Casos de Uso

### Escenario 1: Cliente con Deuda
```
1. Cliente compra por $1000 a crédito
   → Crear cuenta por cobrar: $1000, vencimiento 30 días
   
2. Cliente paga $400 después de 10 días
   → Registrar pago: $400
   → Estado: PARTIAL, Pendiente: $600
   
3. Cliente paga los $600 restantes antes del vencimiento
   → Registrar pago: $600
   → Estado: PAID, Pendiente: $0
```

### Escenario 2: Factura de Proveedor
```
1. Recibo factura de proveedor por $2000
   → Crear cuenta por pagar: $2000, vencimiento 15 días
   → Estado: PENDING
   
2. Pasan 20 días sin pagar
   → Sistema automáticamente: Estado → OVERDUE
   → Aparece en rojo en la interfaz
   
3. Pago la factura
   → Registrar pago: $2000
   → Estado: PAID
```

### Escenario 3: Pagos Parciales Múltiples
```
Cuenta: $5000

Pago 1: $1000 → Pendiente: $4000 (PARTIAL)
Pago 2: $1500 → Pendiente: $2500 (PARTIAL)
Pago 3: $2500 → Pendiente: $0 (PAID)

Historial completo guardado con fechas y referencias
```

---

## 🔐 Seguridad

- ✅ Autenticación requerida (JWT)
- ✅ Aislamiento por business_id (multi-tenant)
- ✅ Soft delete para auditoría
- ✅ Validación de montos
- ✅ Control de permisos
- ✅ Protección CSRF
- ✅ SQL injection prevention (ORM)

---

## 📊 Beneficios del Sistema

1. **Control Financiero Total**
   - Saber exactamente cuánto te deben
   - Saber exactamente cuánto debes
   - Evitar pagos duplicados

2. **Alertas Automáticas**
   - Detecta facturas vencidas
   - Resalta deudas urgentes
   - Estados visuales claros

3. **Historial Completo**
   - Cada pago registrado
   - Fecha, método y referencia
   - Auditoría completa

4. **Análisis Financiero**
   - Resumen en tiempo real
   - Estadísticas de cobros/pagos
   - Identificación de cuentas problema

5. **Integración**
   - Conectado con módulo de Clientes
   - Alineado con sistema de Órdenes
   - Parte del ecosistema completo

---

## 🎯 Próximas Mejoras (Opcionales)

### Reportes Avanzados
- 📈 Gráficos de cuentas por vencer
- 📊 Análisis de antigüedad de saldos
- 📉 Tendencias de cobros/pagos

### Automatizaciones
- 📧 Envío automático de recordatorios
- 🔔 Notificaciones de vencimiento
- 📱 Alertas push

### Exportación
- 📄 Exportar a Excel
- 📋 Exportar a PDF
- 📊 Informes contables

### Integraciones
- 💳 Integración con pasarelas de pago
- 📧 Envío de facturas por email
- 🔗 Conexión con sistemas contables

---

## ✅ Checklist de Implementación

### Backend
- [x] Modelos SQLAlchemy
- [x] Enums de estados
- [x] Schemas Pydantic
- [x] Routers con CRUD completo
- [x] Endpoints de pagos
- [x] Endpoints de resúmenes
- [x] Migraciones ejecutadas
- [x] Integración en main.py
- [x] Validaciones implementadas
- [x] Soft delete activo

### Frontend
- [x] Modelos TypeScript
- [x] Servicios HTTP
- [x] Componente Cuentas por Cobrar
- [x] Componente Cuentas por Pagar
- [x] Templates HTML
- [x] Formularios reactivos
- [x] Modales funcionales
- [x] Tarjetas de resumen
- [x] Filtros por estado
- [x] Rutas configuradas
- [x] Enlaces en menú lateral
- [x] Estilos responsive

### Funcionalidades
- [x] Crear cuentas
- [x] Editar cuentas
- [x] Eliminar cuentas
- [x] Registrar pagos
- [x] Actualización automática de estados
- [x] Cálculo automático de pendientes
- [x] Detección de vencimientos
- [x] Historial de pagos
- [x] Estadísticas en tiempo real
- [x] Filtrado por estados
- [x] Validaciones de negocio

---

## 🎉 Conclusión

**MÓDULO 100% FUNCIONAL Y LISTO PARA PRODUCCIÓN**

El sistema de Cuentas por Cobrar y Cuentas por Pagar está completamente implementado y operativo. Incluye toda la funcionalidad necesaria para una gestión profesional de las finanzas del negocio.

**Características destacadas:**
- ✅ Backend robusto con PostgreSQL
- ✅ Frontend moderno con Angular 19
- ✅ Interfaz intuitiva y responsive
- ✅ Actualización automática de estados
- ✅ Validaciones completas
- ✅ Multi-tenant seguro
- ✅ Soft delete para auditoría

**Listo para usar inmediatamente** 🚀

---

**Fecha de finalización:** 9 de noviembre de 2025  
**Estado:** ✅ COMPLETADO AL 100%  
**Versión:** 1.0.0

