import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, fromEvent, merge, of } from 'rxjs';
import { map, debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { IndexedDbService, PendingSync } from './indexed-db.service';
import { NotificationService } from './notification.service';

@Injectable({
  providedIn: 'root'
})
export class SyncService {
  private onlineSubject = new BehaviorSubject<boolean>(navigator.onLine);
  public online$ = this.onlineSubject.asObservable();
  
  private syncingSubject = new BehaviorSubject<boolean>(false);
  public syncing$ = this.syncingSubject.asObservable();
  
  private pendingCountSubject = new BehaviorSubject<number>(0);
  public pendingCount$ = this.pendingCountSubject.asObservable();

  private syncInProgress = false;
  private syncInterval: any;

  constructor(
    private http: HttpClient,
    private indexedDb: IndexedDbService,
    private notificationService: NotificationService
  ) {
    this.initOnlineStatusMonitoring();
    this.initAutoSync();
    this.updatePendingCount();
  }

  private initOnlineStatusMonitoring(): void {
    // Monitorear cambios en el estado de conexión
    merge(
      fromEvent(window, 'online'),
      fromEvent(window, 'offline')
    ).pipe(
      debounceTime(1000),
      map(() => navigator.onLine),
      distinctUntilChanged()
    ).subscribe(isOnline => {
      this.onlineSubject.next(isOnline);
      console.log(`Estado de conexión: ${isOnline ? 'Online' : 'Offline'}`);
      
      if (isOnline) {
        this.notificationService.success('Conexión restaurada');
        this.syncPendingData();
      } else {
        this.notificationService.warning('Modo offline - Los cambios se sincronizarán cuando haya conexión');
      }
    });
  }

  private initAutoSync(): void {
    // Sincronizar automáticamente cada 30 segundos si hay conexión
    this.syncInterval = setInterval(() => {
      if (this.isOnline() && !this.syncInProgress) {
        this.syncPendingData();
      }
    }, 30000);
  }

  isOnline(): boolean {
    return this.onlineSubject.value;
  }

  async updatePendingCount(): Promise<void> {
    try {
      const pending = await this.indexedDb.getPendingSync();
      this.pendingCountSubject.next(pending.length);
    } catch (error) {
      console.error('Error updating pending count:', error);
    }
  }

  async addPendingOperation(
    type: 'CREATE' | 'UPDATE' | 'DELETE',
    entity: string,
    data: any
  ): Promise<void> {
    try {
      await this.indexedDb.addPendingSync({
        type,
        entity,
        data,
        timestamp: Date.now(),
        retries: 0
      });
      
      await this.updatePendingCount();
      
      // Si estamos online, intentar sincronizar inmediatamente
      if (this.isOnline()) {
        setTimeout(() => this.syncPendingData(), 1000);
      }
    } catch (error) {
      console.error('Error adding pending operation:', error);
      throw error;
    }
  }

  async syncPendingData(): Promise<void> {
    if (this.syncInProgress || !this.isOnline()) {
      return;
    }

    try {
      this.syncInProgress = true;
      this.syncingSubject.next(true);

      const pendingOperations = await this.indexedDb.getPendingSync();
      
      if (pendingOperations.length === 0) {
        return;
      }

      console.log(`Sincronizando ${pendingOperations.length} operaciones pendientes...`);

      let successCount = 0;
      let errorCount = 0;

      for (const operation of pendingOperations) {
        try {
          await this.syncOperation(operation);
          await this.indexedDb.removePendingSync(operation.id!);
          successCount++;
        } catch (error: any) {
          console.error(`Error sincronizando operación ${operation.id}:`, error);
          errorCount++;

          // Incrementar contador de reintentos
          const newRetries = operation.retries + 1;
          
          // Si ha fallado más de 3 veces, informar al usuario
          if (newRetries >= 3) {
            this.notificationService.error(
              `Error sincronizando ${operation.entity}: ${error.message || 'Error desconocido'}`
            );
            // Eliminar después de 3 intentos fallidos
            await this.indexedDb.removePendingSync(operation.id!);
          } else {
            await this.indexedDb.updatePendingSyncRetries(operation.id!, newRetries);
          }
        }
      }

      await this.updatePendingCount();

      if (successCount > 0) {
        this.notificationService.success(`${successCount} operación(es) sincronizada(s)`);
      }

    } catch (error) {
      console.error('Error during sync:', error);
    } finally {
      this.syncInProgress = false;
      this.syncingSubject.next(false);
    }
  }

  private async syncOperation(operation: PendingSync): Promise<void> {
    const { type, entity, data } = operation;

    switch (entity) {
      case 'order':
        return this.syncOrder(type, data);
      case 'order_payment':
        return this.syncOrderPayment(type, data);
      case 'table':
        return this.syncTable(type, data);
      default:
        console.warn(`Entity type not supported for sync: ${entity}`);
    }
  }

  private syncOrder(type: string, data: any): Promise<any> {
    switch (type) {
      case 'CREATE':
        return this.http.post('/api/orders/', data).toPromise();
      case 'UPDATE':
        return this.http.put(`/api/orders/${data.id}/items`, data).toPromise();
      case 'DELETE':
        return this.http.delete(`/api/orders/${data.id}`).toPromise();
      default:
        return Promise.reject(new Error(`Unknown operation type: ${type}`));
    }
  }

  private syncOrderPayment(type: string, data: any): Promise<any> {
    if (type === 'CREATE') {
      return this.http.post(`/api/orders/${data.order_id}/payments`, data.payment).toPromise();
    }
    return Promise.reject(new Error(`Unknown operation type: ${type}`));
  }

  private syncTable(type: string, data: any): Promise<any> {
    if (type === 'UPDATE') {
      return this.http.put(`/api/tables/${data.id}`, data).toPromise();
    }
    return Promise.reject(new Error(`Unknown operation type: ${type}`));
  }

  // Método para verificar conectividad real con el servidor
  async checkServerConnectivity(): Promise<boolean> {
    if (!navigator.onLine) {
      return false;
    }

    try {
      const response = await this.http.get('/health', { 
        observe: 'response',
        headers: { 'Cache-Control': 'no-cache' }
      }).toPromise();
      return response?.status === 200;
    } catch {
      return false;
    }
  }

  destroy(): void {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }
  }
}

