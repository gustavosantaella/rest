import { Injectable } from '@angular/core';
import { Observable, from, of, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { OrderService } from './order.service';
import { SyncService } from './sync.service';
import { IndexedDbService } from './indexed-db.service';
import { Order, CreateOrder, UpdateOrderItems } from '../models/order.model';

@Injectable({
  providedIn: 'root'
})
export class OfflineOrderService {
  constructor(
    private orderService: OrderService,
    private syncService: SyncService,
    private indexedDb: IndexedDbService
  ) {}

  createOrder(order: CreateOrder): Observable<Order> {
    if (this.syncService.isOnline()) {
      // Si estamos online, intentar crear directamente
      return this.orderService.createOrder(order).pipe(
        catchError(error => {
          // Si falla, guardar para sincronizar después
          return this.saveOrderOffline(order);
        })
      );
    } else {
      // Si estamos offline, guardar directamente
      return this.saveOrderOffline(order);
    }
  }

  private saveOrderOffline(order: CreateOrder): Observable<Order> {
    return from(
      this.syncService.addPendingOperation('CREATE', 'order', order)
    ).pipe(
      switchMap(() => {
        // Crear una orden temporal con ID negativo
        const tempOrder: Order = {
          id: -Date.now(), // ID temporal negativo
          table_id: order.table_id,
          status: 'pending',
          notes: order.notes,
          items: order.items.map((item, index) => ({
            id: -(Date.now() + index),
            order_id: -Date.now(),
            product_id: item.product_id,
            menu_item_id: item.menu_item_id,
            quantity: item.quantity,
            unit_price: 0,
            subtotal: 0,
            notes: item.notes,
            source_type: item.source_type
          })),
          payments: [],
          subtotal: 0,
          tax: 0,
          total: 0,
          paid_amount: 0,
          remaining_amount: 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          created_by: 0,
          updated_by: 0
        };
        
        return of(tempOrder);
      })
    );
  }

  updateOrderItems(orderId: number, items: UpdateOrderItems): Observable<Order> {
    if (this.syncService.isOnline()) {
      return this.orderService.updateOrderItems(orderId, items).pipe(
        catchError(error => {
          return this.saveOrderUpdateOffline(orderId, items);
        })
      );
    } else {
      return this.saveOrderUpdateOffline(orderId, items);
    }
  }

  private saveOrderUpdateOffline(orderId: number, items: UpdateOrderItems): Observable<Order> {
    return from(
      this.syncService.addPendingOperation('UPDATE', 'order', {
        id: orderId,
        items: items.items
      })
    ).pipe(
      switchMap(() => {
        // Devolver la orden con los nuevos items
        return this.orderService.getOrder(orderId);
      }),
      catchError(() => {
        // Si no se puede obtener la orden, crear una temporal
        const tempOrder: Order = {
          id: orderId,
          table_id: 0,
          status: 'pending',
          notes: '',
          items: [],
          payments: [],
          subtotal: 0,
          tax: 0,
          total: 0,
          paid_amount: 0,
          remaining_amount: 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          created_by: 0,
          updated_by: 0
        };
        return of(tempOrder);
      })
    );
  }

  addPayment(orderId: number, payment: any): Observable<Order> {
    if (this.syncService.isOnline()) {
      return this.orderService.addPayment(orderId, payment).pipe(
        catchError(error => {
          return this.savePaymentOffline(orderId, payment);
        })
      );
    } else {
      return this.savePaymentOffline(orderId, payment);
    }
  }

  private savePaymentOffline(orderId: number, payment: any): Observable<Order> {
    return from(
      this.syncService.addPendingOperation('CREATE', 'order_payment', {
        order_id: orderId,
        payment
      })
    ).pipe(
      switchMap(() => {
        return this.orderService.getOrder(orderId);
      }),
      catchError(() => {
        // Devolver orden temporal
        const tempOrder: Order = {
          id: orderId,
          table_id: 0,
          status: 'paid',
          notes: '',
          items: [],
          payments: [],
          subtotal: 0,
          tax: 0,
          total: 0,
          paid_amount: 0,
          remaining_amount: 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          created_by: 0,
          updated_by: 0
        };
        return of(tempOrder);
      })
    );
  }

  // Métodos de solo lectura que intentan usar caché
  getOrders(): Observable<Order[]> {
    if (this.syncService.isOnline()) {
      return this.orderService.getOrders().pipe(
        switchMap(orders => {
          // Guardar en caché
          return from(
            this.indexedDb.setCachedData('orders', orders, 1000 * 60 * 5) // 5 minutos
          ).pipe(
            switchMap(() => of(orders))
          );
        }),
        catchError(() => this.getOrdersFromCache())
      );
    } else {
      return this.getOrdersFromCache();
    }
  }

  private getOrdersFromCache(): Observable<Order[]> {
    return from(
      this.indexedDb.getCachedData<Order[]>('orders')
    ).pipe(
      switchMap(orders => orders ? of(orders) : of([]))
    );
  }

  getOrder(id: number): Observable<Order | null> {
    if (this.syncService.isOnline()) {
      return this.orderService.getOrder(id).pipe(
        switchMap(order => {
          return from(
            this.indexedDb.setCachedData(`order_${id}`, order, 1000 * 60 * 5)
          ).pipe(
            switchMap(() => of(order))
          );
        }),
        catchError(() => this.getOrderFromCache(id))
      );
    } else {
      return this.getOrderFromCache(id);
    }
  }

  private getOrderFromCache(id: number): Observable<Order | null> {
    return from(
      this.indexedDb.getCachedData<Order>(`order_${id}`)
    );
  }
}

