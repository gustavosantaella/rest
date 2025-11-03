# ⚙️ Módulo de Configuración del Negocio

## 🎯 Descripción

Módulo completo para gestionar la información legal y administrativa del negocio, incluyendo datos fiscales y gestión de socios con porcentajes de participación.

## ✨ Características

### 📋 Información del Negocio
- **Nombre Comercial**: Cómo se conoce el negocio
  - 🎯 Aparece en el **sidebar** del sistema
  - 🎯 Aparece en el **top bar** como título
  - 🎯 Aparece en el **título de la pestaña** del navegador
  - 🎯 Iniciales se muestran en el logo cuando sidebar está colapsado
- **Razón Social**: Nombre legal registrado
- **RIF/NIT/Tax ID**: Identificación fiscal
- **Contacto**: Teléfono, email, dirección
- **Configuración Fiscal**: 
  - Tasa de impuesto (IVA)
  - Moneda de operación
- **Logo**: URL de la imagen del negocio

### 👥 Gestión de Socios
- **Usuarios Administradores como Socios**
- **Porcentaje de Participación** (debe sumar 100%)
- **Monto de Inversión** (opcional)
- **Fecha de Ingreso**
- **Estado**: Activo/Inactivo
- **Notas**: Información adicional

## 🔒 Permisos

**Solo ADMIN** puede acceder y gestionar este módulo.

## 📊 Validaciones Automáticas

### 1. Porcentaje Total
```
✅ El sistema verifica que la suma de participaciones = 100%
❌ No permite agregar socios si excedería el 100%
💡 Muestra porcentaje disponible en tiempo real
```

### 2. Socios Deben ser Administradores
```
✅ Solo usuarios con rol ADMIN pueden ser socios
❌ No se puede agregar Waiter, Cashier o Chef como socios
```

### 3. RIF Único
```
✅ El RIF debe ser único en el sistema
❌ No se permiten duplicados
```

## 🎯 Casos de Uso

### Caso 1: Negocio Individual
```
Información del Negocio:
  Nombre: "Restaurante El Sabor"
  Razón Social: "Restaurante El Sabor C.A."
  RIF: J-12345678-9
  
Socios:
  - Juan Pérez (admin) - 100% - $50,000
```

### Caso 2: Sociedad de 2 Personas
```
Información del Negocio:
  Nombre: "Pizzería Bella Napoli"
  Razón Social: "Bella Napoli S.R.L."
  RIF: J-98765432-1
  
Socios:
  - María García (admin) - 60% - $60,000
  - Pedro López (admin) - 40% - $40,000
  
Total: 100% ✅
```

### Caso 3: Sociedad de 3 Personas
```
Información del Negocio:
  Nombre: "Café Express"
  RIF: J-55555555-5
  
Socios:
  - Ana Martínez (admin) - 50% - $100,000
  - Carlos Ruiz (admin) - 30% - $60,000
  - Luis Fernández (admin) - 20% - $40,000
  
Total: 100% ✅
```

## 🔄 Flujo de Configuración

### Primera Vez:
```
1. Login como admin
2. Ve a "Configuración" (icono de engranaje)
3. Llena información del negocio
4. Click "Guardar Configuración"
5. Agrega socios:
   a. Click "+ Agregar Socio"
   b. Selecciona usuario admin
   c. Define porcentaje (ej: 50%)
   d. Opcional: monto de inversión
   e. Guardar
6. Repite hasta que sume 100%
```

### Actualización:
```
1. Ve a Configuración
2. Modifica campos necesarios
3. Click "Actualizar Configuración"
```

## 💡 Características Especiales

### 1. Validación en Tiempo Real
```html
Disponible: 45.00%
```
Muestra cuánto porcentaje queda disponible mientras agregas socios.

### 2. Barra de Progreso Visual
Cada socio muestra su porcentaje con una barra visual:
```
Juan Pérez        50%
[████████████████████░░░░░░░░░]
```

### 3. Alerta de Participación
```
Participación total: 95%
(Debe sumar 100%) ❌
```

### 4. Solo Admin en Sidebar
El menú "Configuración" solo aparece para usuarios Administradores.

## 📋 Campos Detallados

### Información del Negocio

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| Nombre Comercial | Texto | ✅ Sí | Nombre del local |
| Razón Social | Texto | ❌ No | Nombre legal |
| RIF | Texto | ❌ No | ID Fiscal |
| Teléfono | Texto | ❌ No | Contacto |
| Email | Email | ❌ No | Correo oficial |
| Dirección | Textarea | ❌ No | Ubicación |
| Tasa Impuesto | Número | ✅ Sí | % IVA (default: 16) |
| Moneda | Select | ✅ Sí | USD, EUR, VES, etc. |
| Logo URL | URL | ❌ No | Imagen del logo |

### Socios

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| Usuario | Select | ✅ Sí | Usuario admin |
| % Participación | Número | ✅ Sí | 0-100% |
| Inversión | Número | ❌ No | Monto invertido |
| Activo | Checkbox | ✅ Sí | Si está activo |
| Notas | Textarea | ❌ No | Info adicional |

## 🎨 Interfaz de Usuario

### Vista Principal
```
┌────────────────────────────────────┐
│ ⚙️ Configuración del Negocio       │
├────────────────────────────────────┤
│ Información del Negocio            │
│                                    │
│ Nombre: [Restaurante El Sabor]    │
│ RIF: [J-12345678-9]                │
│ Tasa IVA: [16]%                    │
│                                    │
│ [Actualizar Configuración]         │
├────────────────────────────────────┤
│ Socios del Negocio                 │
│ Participación total: 100% ✅       │
│                                    │
│ ┌──────────┬──────────┬──────────┐│
│ │Juan 50%  │María 30% │Luis 20%  ││
│ │$100,000  │$60,000   │$40,000   ││
│ │[Edit][X] │[Edit][X] │[Edit][X] ││
│ └──────────┴──────────┴──────────┘│
│                                    │
│ [+ Agregar Socio]                  │
└────────────────────────────────────┘
```

## 🔐 Seguridad

### Restricciones:
- ✅ Solo ADMIN puede acceder
- ✅ Solo ADMIN puede ser socio
- ✅ Validación de porcentajes
- ✅ Un solo registro de configuración
- ✅ RIF único

## 📊 Validaciones del Sistema

### Al Agregar Socio:
```python
# Backend valida:
1. Usuario existe ✓
2. Usuario es Admin ✓
3. Porcentaje + total <= 100% ✓
4. Configuración existe ✓
```

### Al Actualizar Socio:
```python
# Backend valida:
1. Socio existe ✓
2. Nuevo porcentaje + otros <= 100% ✓
```

## 🚀 Uso Práctico

### Ejemplo: Restaurante Familiar

**Paso 1: Crear Usuarios Admin**
```
1. Usuario: juan_admin (Admin)
2. Usuario: maria_admin (Admin)
3. Usuario: pedro_admin (Admin)
```

**Paso 2: Configurar Negocio**
```
Nombre: "Restaurante Familiar Los Pérez"
RIF: J-11111111-1
Tasa IVA: 16%
```

**Paso 3: Agregar Socios**
```
1. Juan Pérez - 40% - $80,000
2. María Pérez - 35% - $70,000
3. Pedro Pérez - 25% - $50,000

Total: 100% ✅
Total Inversión: $200,000
```

## 📈 Usos Futuros

Esta configuración se puede usar para:

### Actual:
- ✅ Información del negocio centralizada
- ✅ Control de socios y participaciones
- ✅ Tasa de impuesto configurable

### Futuro:
- 📊 **Reportes de Ganancias por Socio**
  - Calcular ganancia según % participación
  - Distribuir utilidades automáticamente
  
- 📄 **Facturas Personalizadas**
  - Incluir RIF en facturas
  - Logo del negocio
  - Dirección legal
  
- 💰 **Dashboard de Socios**
  - Ver inversión vs ganancias
  - ROI individual
  - Historial de pagos

- 📧 **Notificaciones**
  - Enviar reportes mensuales a socios
  - Alertas de rendimiento

## 🎯 Mejores Prácticas

### ✅ DO:
- Configura tu negocio antes de agregar socios
- Asegúrate que todos los socios sean usuarios admin
- Verifica que el porcentaje total sea exactamente 100%
- Documenta la inversión de cada socio
- Mantén actualizada la información de contacto

### ❌ DON'T:
- No agregues usuarios no-admin como socios
- No dejes la participación sin sumar 100%
- No uses RIF duplicados
- No elimines la configuración una vez creada

## 📱 API Endpoints

```
GET    /api/configuration          - Obtener configuración
POST   /api/configuration          - Crear configuración
PUT    /api/configuration          - Actualizar configuración

GET    /api/configuration/partners - Listar socios
POST   /api/configuration/partners - Agregar socio
PUT    /api/configuration/partners/{id} - Actualizar socio
DELETE /api/configuration/partners/{id} - Eliminar socio
```

## 🔄 Migraciones

Si ya tienes el sistema corriendo:

```bash
cd backend

# Las tablas se crean automáticamente al reiniciar
python run.py
```

Verás en los logs:
```
Creating table business_configuration
Creating table partners
```

## ✨ Características EXTRA

1. **Tooltips Informativos**: Cada campo explica qué ingresar
2. **Validación en Tiempo Real**: Muestra % disponible
3. **Barra de Progreso Visual**: Para cada socio
4. **Cálculo Automático**: Total de participación
5. **Solo Admin**: Protección de acceso

---

**Módulo de Configuración completamente implementado** ✅

Accede en: http://localhost:4200/configuration

