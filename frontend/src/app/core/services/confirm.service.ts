import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';

export interface ConfirmOptions {
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  type?: 'danger' | 'warning' | 'info';
}

export interface ConfirmResult {
  confirmed: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ConfirmService {
  private confirmSubject = new Subject<ConfirmOptions | null>();
  private resultSubject = new Subject<ConfirmResult>();

  public confirm$ = this.confirmSubject.asObservable();

  /**
   * Muestra un diálogo de confirmación
   * @param options Opciones del diálogo
   * @returns Observable que emite true si se confirma, false si se cancela
   */
  confirm(options: ConfirmOptions): Observable<boolean> {
    this.confirmSubject.next({
      ...options,
      confirmText: options.confirmText || 'Confirmar',
      cancelText: options.cancelText || 'Cancelar',
      type: options.type || 'warning'
    });

    return new Observable(observer => {
      const subscription = this.resultSubject.subscribe(result => {
        observer.next(result.confirmed);
        observer.complete();
        subscription.unsubscribe();
      });
    });
  }

  /**
   * Cierra el diálogo con el resultado
   * @param confirmed true si se confirmó, false si se canceló
   */
  resolve(confirmed: boolean): void {
    this.resultSubject.next({ confirmed });
    this.confirmSubject.next(null);
  }

  /**
   * Método de ayuda para confirmar eliminación
   * @param itemName Nombre del elemento a eliminar
   * @returns Observable que emite true si se confirma
   */
  confirmDelete(itemName: string): Observable<boolean> {
    return this.confirm({
      title: 'Confirmar eliminación',
      message: `¿Estás seguro de que deseas eliminar "${itemName}"? Esta acción no se puede deshacer.`,
      confirmText: 'Eliminar',
      cancelText: 'Cancelar',
      type: 'danger'
    });
  }

  /**
   * Método de ayuda para confirmar cambios
   * @param message Mensaje de confirmación
   * @returns Observable que emite true si se confirma
   */
  confirmChanges(message: string): Observable<boolean> {
    return this.confirm({
      title: 'Confirmar cambios',
      message: message,
      confirmText: 'Confirmar',
      cancelText: 'Cancelar',
      type: 'info'
    });
  }
}

