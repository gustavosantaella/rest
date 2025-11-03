import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface Notification {
  id: number;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notificationsSubject = new BehaviorSubject<Notification[]>([]);
  public notifications$ = this.notificationsSubject.asObservable();
  private nextId = 1;
  
  show(type: Notification['type'], message: string, duration: number = 5000): void {
    const notification: Notification = {
      id: this.nextId++,
      type,
      message,
      duration
    };
    
    const currentNotifications = this.notificationsSubject.value;
    this.notificationsSubject.next([...currentNotifications, notification]);
    
    if (duration > 0) {
      setTimeout(() => {
        this.remove(notification.id);
      }, duration);
    }
  }
  
  success(message: string, duration?: number): void {
    this.show('success', message, duration);
  }
  
  error(message: string, duration?: number): void {
    this.show('error', message, duration);
  }
  
  warning(message: string, duration?: number): void {
    this.show('warning', message, duration);
  }
  
  info(message: string, duration?: number): void {
    this.show('info', message, duration);
  }
  
  remove(id: number): void {
    const currentNotifications = this.notificationsSubject.value;
    this.notificationsSubject.next(currentNotifications.filter(n => n.id !== id));
  }
  
  clear(): void {
    this.notificationsSubject.next([]);
  }
}

