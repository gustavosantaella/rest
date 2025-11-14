# Ejemplo de Uso del Servicio Offline

## 🎯 Caso de Uso: Crear una Orden en Modo Offline

### Opción 1: Usando OfflineOrderService (Recomendado)

Este es el enfoque más simple y recomendado. El servicio maneja automáticamente el modo offline/online.

```typescript
import { Component } from '@angular/core';
import { OfflineOrderService } from '../../core/services/offline-order.service';
import { CreateOrder } from '../../core/models/order.model';
import { NotificationService } from '../../core/services/notification.service';

@Component({
  selector: 'app-my-component',
  // ...
})
export class MyComponent {
  constructor(
    private offlineOrderService: OfflineOrderService,
    private notificationService: NotificationService
  ) {}

  createOrder(): void {
    const orderData: CreateOrder = {
      table_id: 5,
      notes: 'Sin cebolla',
      items: [
        {
          product_id: 10,
          quantity: 2,
          notes: '',
          source_type: 'product'
        }
      ],
      payments: []
    };

    // El servicio maneja automáticamente el modo offline
    this.offlineOrderService.createOrder(orderData).subscribe({
      next: (order) => {
        console.log('Orden creada:', order);
        this.notificationService.success('Orden creada exitosamente');
        // Si estás offline, order.id será negativo (temporal)
        // Se sincronizará automáticamente cuando haya conexión
      },
      error: (error) => {
        console.error('Error creando orden:', error);
        this.notificationService.error('Error al crear la orden');
      }
    });
  }
}
```

### Opción 2: Manejo Manual con SyncService

Si necesitas más control sobre el proceso de sincronización:

```typescript
import { Component } from '@angular/core';
import { SyncService } from '../../core/services/sync.service';
import { OrderService } from '../../core/services/order.service';
import { NotificationService } from '../../core/services/notification.service';

@Component({
  selector: 'app-my-component',
  // ...
})
export class MyComponent {
  constructor(
    private syncService: SyncService,
    private orderService: OrderService,
    private notificationService: NotificationService
  ) {}

  async createOrderWithManualSync(): Promise<void> {
    const orderData = {
      table_id: 5,
      notes: 'Sin cebolla',
      items: [
        {
          product_id: 10,
          quantity: 2,
          notes: '',
          source_type: 'product'
        }
      ],
      payments: []
    };

    if (this.syncService.isOnline()) {
      // Online: Crear directamente
      this.orderService.createOrder(orderData).subscribe({
        next: (order) => {
          console.log('Orden creada online:', order);
          this.notificationService.success('Orden creada');
        },
        error: async (error) => {
          // Si falla, guardar para sincronizar después
          console.error('Error creando orden online, guardando offline:', error);
          await this.syncService.addPendingOperation('CREATE', 'order', orderData);
          this.notificationService.warning('Orden guardada para sincronización');
        }
      });
    } else {
      // Offline: Guardar para sincronizar después
      try {
        await this.syncService.addPendingOperation('CREATE', 'order', orderData);
        this.notificationService.success('Orden guardada (se sincronizará automáticamente)');
      } catch (error) {
        console.error('Error guardando orden offline:', error);
        this.notificationService.error('Error guardando la orden');
      }
    }
  }
}
```

### Opción 3: Con IndexedDB Directamente

Para casos muy específicos donde necesitas acceso directo a IndexedDB:

```typescript
import { Component } from '@angular/core';
import { IndexedDbService } from '../../core/services/indexed-db.service';
import { NotificationService } from '../../core/services/notification.service';

@Component({
  selector: 'app-my-component',
  // ...
})
export class MyComponent {
  constructor(
    private indexedDb: IndexedDbService,
    private notificationService: NotificationService
  ) {}

  async saveDataToCache(): Promise<void> {
    try {
      // Guardar en caché por 1 hora
      await this.indexedDb.setCachedData(
        'my-custom-data',
        { someData: 'value' },
        1000 * 60 * 60
      );
      
      console.log('Datos guardados en caché');
    } catch (error) {
      console.error('Error guardando en caché:', error);
    }
  }

  async loadDataFromCache(): Promise<void> {
    try {
      const data = await this.indexedDb.getCachedData('my-custom-data');
      
      if (data) {
        console.log('Datos recuperados del caché:', data);
      } else {
        console.log('No hay datos en caché o expiraron');
      }
    } catch (error) {
      console.error('Error cargando del caché:', error);
    }
  }
}
```

## 🔔 Monitorear el Estado de Conexión

### En el Template (HTML)

```html
<!-- Mostrar mensaje si está offline -->
<div *ngIf="!(syncService.online$ | async)" class="alert alert-warning">
  ⚠️ Estás trabajando sin conexión. Los cambios se sincronizarán automáticamente.
</div>

<!-- Mostrar si está sincronizando -->
<div *ngIf="syncService.syncing$ | async" class="alert alert-info">
  🔄 Sincronizando datos...
</div>

<!-- Mostrar operaciones pendientes -->
<div *ngIf="(syncService.pendingCount$ | async)! > 0" class="alert alert-info">
  📊 Hay {{ syncService.pendingCount$ | async }} operación(es) pendiente(s) de sincronizar
</div>
```

### En el Componente (TypeScript)

```typescript
import { Component, OnInit } from '@angular/core';
import { SyncService } from '../../core/services/sync.service';

@Component({
  selector: 'app-my-component',
  // ...
})
export class MyComponent implements OnInit {
  isOnline = true;
  isSyncing = false;
  pendingCount = 0;

  constructor(public syncService: SyncService) {}

  ngOnInit(): void {
    // Suscribirse al estado de conexión
    this.syncService.online$.subscribe(online => {
      this.isOnline = online;
      console.log('Estado de conexión:', online ? 'Online' : 'Offline');
    });

    // Suscribirse al estado de sincronización
    this.syncService.syncing$.subscribe(syncing => {
      this.isSyncing = syncing;
      console.log('Sincronizando:', syncing);
    });

    // Suscribirse al contador de operaciones pendientes
    this.syncService.pendingCount$.subscribe(count => {
      this.pendingCount = count;
      console.log('Operaciones pendientes:', count);
    });
  }

  // Forzar sincronización manual
  async forceSyncNow(): Promise<void> {
    if (this.isOnline && !this.isSyncing) {
      await this.syncService.syncPendingData();
    }
  }
}
```

## 🎨 Componente de Ejemplo Completo

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { OfflineOrderService } from '../../core/services/offline-order.service';
import { SyncService } from '../../core/services/sync.service';
import { NotificationService } from '../../core/services/notification.service';
import { CreateOrder, Order } from '../../core/models/order.model';

@Component({
  selector: 'app-offline-example',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container">
      <h2>Ejemplo de Orden Offline</h2>
      
      <!-- Estado de conexión -->
      <div class="status-bar">
        <span [class.online]="isOnline" [class.offline]="!isOnline">
          {{ isOnline ? '🟢 Online' : '🔴 Offline' }}
        </span>
        <span *ngIf="isSyncing">🔄 Sincronizando...</span>
        <span *ngIf="pendingCount > 0">
          📊 {{ pendingCount }} pendiente(s)
        </span>
      </div>

      <!-- Formulario de orden -->
      <div class="form">
        <input 
          type="number" 
          [(ngModel)]="tableId" 
          placeholder="ID de Mesa"
          class="input">
        
        <textarea 
          [(ngModel)]="notes" 
          placeholder="Notas"
          class="input"></textarea>
        
        <button (click)="createOrder()" class="btn-primary">
          Crear Orden
        </button>

        <button 
          *ngIf="isOnline && pendingCount > 0" 
          (click)="forceSyncNow()"
          class="btn-secondary">
          Sincronizar Ahora
        </button>
      </div>

      <!-- Lista de órdenes -->
      <div class="orders-list">
        <h3>Órdenes</h3>
        <div *ngFor="let order of orders" class="order-card">
          <strong>Orden #{{ order.id }}</strong>
          <span>Mesa: {{ order.table_id }}</span>
          <span>Estado: {{ order.status }}</span>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .status-bar {
      padding: 12px;
      background: #f0f0f0;
      border-radius: 8px;
      margin-bottom: 20px;
      display: flex;
      gap: 12px;
    }
    .online { color: green; }
    .offline { color: red; }
    .input {
      width: 100%;
      padding: 8px;
      margin-bottom: 12px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  `]
})
export class OfflineExampleComponent implements OnInit, OnDestroy {
  isOnline = true;
  isSyncing = false;
  pendingCount = 0;
  
  tableId = 1;
  notes = '';
  orders: Order[] = [];

  private subscriptions: Subscription[] = [];

  constructor(
    private offlineOrderService: OfflineOrderService,
    private syncService: SyncService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    // Monitorear estado de conexión
    this.subscriptions.push(
      this.syncService.online$.subscribe(online => {
        this.isOnline = online;
      })
    );

    this.subscriptions.push(
      this.syncService.syncing$.subscribe(syncing => {
        this.isSyncing = syncing;
      })
    );

    this.subscriptions.push(
      this.syncService.pendingCount$.subscribe(count => {
        this.pendingCount = count;
      })
    );

    // Cargar órdenes
    this.loadOrders();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  createOrder(): void {
    const orderData: CreateOrder = {
      table_id: this.tableId,
      notes: this.notes || undefined,
      items: [
        {
          product_id: 1,
          quantity: 1,
          notes: '',
          source_type: 'product'
        }
      ],
      payments: []
    };

    this.offlineOrderService.createOrder(orderData).subscribe({
      next: (order) => {
        console.log('✅ Orden creada:', order);
        this.notificationService.success(
          this.isOnline 
            ? 'Orden creada' 
            : 'Orden guardada (se sincronizará)'
        );
        this.orders.unshift(order);
        this.notes = '';
      },
      error: (error) => {
        console.error('❌ Error:', error);
        this.notificationService.error('Error al crear orden');
      }
    });
  }

  loadOrders(): void {
    this.offlineOrderService.getOrders().subscribe({
      next: (orders) => {
        this.orders = orders;
      },
      error: (error) => {
        console.error('Error cargando órdenes:', error);
      }
    });
  }

  async forceSyncNow(): Promise<void> {
    await this.syncService.syncPendingData();
  }
}
```

## 📋 Checklist de Implementación

Cuando implementes funcionalidad offline en un nuevo componente:

- [ ] Importar `OfflineOrderService` en lugar de `OrderService` directamente
- [ ] Importar `SyncService` para monitorear el estado de conexión
- [ ] Suscribirse a `syncService.online$` para mostrar el estado de conexión
- [ ] Manejar IDs temporales (negativos) en las respuestas offline
- [ ] Mostrar notificaciones apropiadas según el estado de conexión
- [ ] Probar la funcionalidad en modo offline (DevTools > Network > Offline)
- [ ] Verificar que la sincronización funcione al recuperar la conexión
- [ ] Considerar qué hacer con datos obsoletos del caché
- [ ] Implementar lógica de refresco cuando se recupere la conexión

## 🧪 Probar la Funcionalidad Offline

### 1. Simular Offline en Chrome DevTools
1. Abre DevTools (F12)
2. Ve a la pestaña **Network**
3. En el dropdown que dice "No throttling", selecciona **Offline**
4. Intenta crear una orden
5. Verifica que se guarde localmente
6. Cambia a **Online**
7. Espera 30 segundos o fuerza sincronización
8. Verifica que la orden se haya creado en el servidor

### 2. Inspeccionar IndexedDB
1. DevTools > **Application**
2. **Storage** > **IndexedDB** > **RestaurantPOS**
3. Ve los stores:
   - `pendingSync`: Operaciones pendientes
   - `cachedData`: Datos en caché
   - `pendingOrders`: Órdenes temporales

### 3. Ver Service Worker
1. DevTools > **Application**
2. **Service Workers**
3. Verifica que esté activo
4. Click en "Update" para actualizar
5. Marca "Update on reload" para desarrollo

## 💡 Tips y Mejores Prácticas

1. **Siempre usar OfflineOrderService** para operaciones que modifiquen datos
2. **Mostrar feedback visual** del estado de conexión
3. **Informar al usuario** cuando esté trabajando offline
4. **No asumir IDs**: Los IDs temporales son negativos
5. **Recargar datos** después de sincronización exitosa
6. **Manejar conflictos**: Considerar qué pasa si dos dispositivos modifican lo mismo
7. **Límites de almacenamiento**: No guardar archivos grandes en IndexedDB
8. **Testar exhaustivamente**: Probar escenarios de pérdida de conexión inesperada







