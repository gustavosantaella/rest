# 🔄 Implementación de Métodos de Pago

## ✅ Backend Completado

1. **Modelo PaymentMethod** (`backend/app/models/payment_method.py`)
   - ✅ 6 tipos: pago_movil, transferencia, efectivo, bolivares, dolares, euros
   - ✅ Campos dinámicos según tipo
   - ✅ Validación de campos requeridos

2. **Schemas Pydantic** (`backend/app/schemas/payment_method.py`)
   - ✅ Validaciones automáticas según tipo
   - ✅ Create, Update, Response schemas

3. **Router API** (`backend/app/routers/payment_methods.py`)
   - ✅ GET `/api/payment-methods/` - Listar todos
   - ✅ GET `/api/payment-methods/active` - Solo activos
   - ✅ POST `/api/payment-methods/` - Crear (Admin)
   - ✅ PUT `/api/payment-methods/{id}` - Actualizar (Admin)
   - ✅ DELETE `/api/payment-methods/{id}` - Eliminar (Admin)

## ✅ Frontend - Modelos y Servicios

1. **Interfaces TypeScript** (`frontend/src/app/core/models/payment-method.model.ts`)
   - ✅ PaymentMethodType enum
   - ✅ PaymentMethod interface
   - ✅ PaymentMethodCreate/Update interfaces
   - ✅ PAYMENT_METHOD_LABELS

2. **Servicio** (`frontend/src/app/core/services/payment-method.service.ts`)
   - ✅ getPaymentMethods()
   - ✅ getActivePaymentMethods()
   - ✅ createPaymentMethod()
   - ✅ updatePaymentMethod()
   - ✅ deletePaymentMethod()

## 🚧 Pendiente - Frontend UI

### 1. Componente de Configuración

Agregar al `configuration.component.ts`:

```typescript
import { PaymentMethod, PaymentMethodType, PAYMENT_METHOD_LABELS } from '../../core/models/payment-method.model';
import { PaymentMethodService } from '../../core/services/payment-method.service';

// En la clase:
private paymentMethodService = inject(PaymentMethodService);
paymentMethods: PaymentMethod[] = [];
showPaymentMethodModal = false;
editingPaymentMethod: PaymentMethod | null = null;
paymentMethodForm!: FormGroup;
selectedPaymentType: string = '';
PaymentMethodType = PaymentMethodType;

// En initForms():
this.paymentMethodForm = this.fb.group({
  type: ['', Validators.required],
  name: ['', Validators.required],
  phone: [''],
  dni: [''],
  bank: [''],
  account_holder: [''],
  account_number: [''],
  is_active: [true]
});

// En loadData():
this.paymentMethodService.getPaymentMethods().subscribe({
  next: (methods) => {
    this.paymentMethods = methods;
  }
});

// Métodos adicionales:
openPaymentMethodModal(method?: PaymentMethod): void {
  this.editingPaymentMethod = method || null;
  
  if (method) {
    this.selectedPaymentType = method.type;
    this.paymentMethodForm.patchValue(method);
  } else {
    this.paymentMethodForm.reset({ is_active: true });
    this.selectedPaymentType = '';
  }
  
  this.showPaymentMethodModal = true;
}

closePaymentMethodModal(): void {
  this.showPaymentMethodModal = false;
  this.editingPaymentMethod = null;
  this.selectedPaymentType = '';
}

onPaymentTypeChange(): void {
  const type = this.paymentMethodForm.get('type')?.value;
  this.selectedPaymentType = type;
  
  // Limpiar campos
  this.paymentMethodForm.patchValue({
    phone: '',
    dni: '',
    bank: '',
    account_holder: '',
    account_number: ''
  });
  
  // Configurar validadores según tipo
  if (type === 'pago_movil') {
    this.setRequiredFields(['phone', 'dni', 'bank', 'account_holder']);
  } else if (type === 'transferencia') {
    this.setRequiredFields(['account_number', 'dni', 'bank', 'account_holder']);
  } else {
    this.clearRequiredFields();
  }
}

private setRequiredFields(fields: string[]): void {
  fields.forEach(field => {
    this.paymentMethodForm.get(field)?.setValidators(Validators.required);
    this.paymentMethodForm.get(field)?.updateValueAndValidity();
  });
}

private clearRequiredFields(): void {
  ['phone', 'dni', 'bank', 'account_holder', 'account_number'].forEach(field => {
    this.paymentMethodForm.get(field)?.clearValidators();
    this.paymentMethodForm.get(field)?.updateValueAndValidity();
  });
}

savePaymentMethod(): void {
  if (this.paymentMethodForm.invalid) return;
  
  const data = this.paymentMethodForm.value;
  
  if (this.editingPaymentMethod) {
    this.paymentMethodService.updatePaymentMethod(this.editingPaymentMethod.id, data).subscribe({
      next: () => {
        this.loadData();
        this.closePaymentMethodModal();
      }
    });
  } else {
    this.paymentMethodService.createPaymentMethod(data).subscribe({
      next: () => {
        this.loadData();
        this.closePaymentMethodModal();
      }
    });
  }
}

deletePaymentMethod(method: PaymentMethod): void {
  if (confirm(`¿Eliminar método de pago "${method.name}"?`)) {
    this.paymentMethodService.deletePaymentMethod(method.id).subscribe({
      next: () => {
        this.loadData();
      }
    });
  }
}

getPaymentMethodLabel(type: string): string {
  return PAYMENT_METHOD_LABELS[type as PaymentMethodType] || type;
}

getPaymentMethodIcon(type: string): string {
  const icons: Record<string, string> = {
    'pago_movil': '💳',
    'transferencia': '🏦',
    'efectivo': '💵',
    'bolivares': 'Bs',
    'dolares': '$',
    'euros': '€'
  };
  return icons[type] || '💰';
}
```

### 2. Modelo de Order - Agregar Pagos

Crear `OrderPayment` interface en `order.model.ts`:

```typescript
export interface OrderPayment {
  payment_method_id: number;
  payment_method_name?: string;
  amount: number;
  reference?: string;  // Número de referencia
}

// Actualizar Order interface:
export interface Order {
  // ... campos existentes
  payments?: OrderPayment[];  // Nuevo campo
  payment_status?: 'pending' | 'partial' | 'paid';
}
```

### 3. Actualizar Backend Order Model

Crear tabla `order_payments`:

```python
# backend/app/models/order_payment.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OrderPayment(Base):
    __tablename__ = "order_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    amount = Column(Float, nullable=False)
    reference = Column(String, nullable=True)  # Número de referencia
    
    # Relationships
    order = relationship("Order", back_populates="payments")
    payment_method = relationship("PaymentMethod")
```

### 4. Componente de Órdenes - UI

Agregar sección de pagos en `orders.component.html`:

```html
<!-- En el modal de orden -->
<div class="mb-4">
  <label class="block text-sm font-medium text-gray-700 mb-2">Métodos de Pago *</label>
  
  <!-- Botón para agregar pago -->
  <button type="button" (click)="addPayment()" class="btn-secondary mb-2">
    + Agregar Pago
  </button>
  
  <!-- Lista de pagos -->
  <div class="space-y-2">
    <div *ngFor="let payment of orderPayments; let i = index" class="flex items-center space-x-2 p-2 border rounded">
      <select [(ngModel)]="payment.payment_method_id" class="input-field flex-1">
        <option value="">Método de pago</option>
        <option *ngFor="let method of activePaymentMethods" [value]="method.id">
          {{ method.name }}
        </option>
      </select>
      
      <input 
        type="number" 
        [(ngModel)]="payment.amount" 
        placeholder="Monto"
        class="input-field w-32"
      />
      
      <input 
        type="text" 
        [(ngModel)]="payment.reference" 
        placeholder="Referencia (opcional)"
        class="input-field w-40"
      />
      
      <button type="button" (click)="removePayment(i)" class="btn-danger">
        ✕
      </button>
    </div>
  </div>
  
  <!-- Total vs Pagado -->
  <div class="mt-2 text-sm">
    <span>Total: ${{ calculateTotal() }}</span>
    <span class="ml-4">Pagado: ${{ calculatePaidAmount() }}</span>
    <span class="ml-4" [class.text-green-600]="isFullyPaid()" [class.text-red-600]="!isFullyPaid()">
      {{ isFullyPaid() ? '✓ Completo' : '⚠ Falta: $' + (calculateTotal() - calculatePaidAmount()).toFixed(2) }}
    </span>
  </div>
</div>
```

## 📋 Próximos Pasos

1. ✅ Terminar modal de métodos de pago en configuración
2. ⏳ Migración BD para crear tabla `payment_methods`
3. ⏳ Crear tabla `order_payments` en backend
4. ⏳ Actualizar endpoints de Orders para manejar pagos
5. ⏳ Actualizar UI de Orders para seleccionar métodos
6. ⏳ Implementar lógica de pagos mixtos
7. ⏳ Validar que la suma de pagos = total de orden

## 🎯 Objetivo Final

- ✅ Un sistema completo donde:
  - Admin configura métodos de pago disponibles
  - Al crear orden, se selecciona método(s) de pago
  - Soporte para pago mixto (varios métodos)
  - Validación automática de montos
  - Historial de pagos por orden

