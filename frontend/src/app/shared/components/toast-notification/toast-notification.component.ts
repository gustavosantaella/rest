import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificationService, Notification } from '../../../core/services/notification.service';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-toast-notification',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="toast-container">
      <div 
        *ngFor="let notification of notifications"
        class="toast toast-{{notification.type}}"
        [@slideIn]
        (click)="close(notification.id)"
      >
        <div class="toast-icon">
          <span *ngIf="notification.type === 'success'">✓</span>
          <span *ngIf="notification.type === 'error'">✕</span>
          <span *ngIf="notification.type === 'warning'">⚠</span>
          <span *ngIf="notification.type === 'info'">ℹ</span>
        </div>
        <div class="toast-message">{{ notification.message }}</div>
        <button class="toast-close" (click)="close(notification.id)">×</button>
      </div>
    </div>
  `,
  styles: [`
    .toast-container {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-width: 400px;
    }

    .toast {
      display: flex;
      align-items: center;
      padding: 16px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      background: white;
      cursor: pointer;
      transition: transform 0.2s;
      position: relative;
      overflow: hidden;
    }

    .toast:hover {
      transform: translateX(-5px);
    }

    .toast-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      margin-right: 12px;
      font-size: 18px;
      font-weight: bold;
      flex-shrink: 0;
    }

    .toast-message {
      flex: 1;
      font-size: 14px;
      line-height: 1.4;
      color: #333;
    }

    .toast-close {
      background: none;
      border: none;
      font-size: 24px;
      line-height: 1;
      cursor: pointer;
      color: #999;
      padding: 0;
      margin-left: 8px;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .toast-close:hover {
      color: #666;
    }

    /* Success Toast */
    .toast-success {
      border-left: 4px solid #10b981;
    }

    .toast-success .toast-icon {
      background-color: #d1fae5;
      color: #10b981;
    }

    /* Error Toast */
    .toast-error {
      border-left: 4px solid #ef4444;
    }

    .toast-error .toast-icon {
      background-color: #fee2e2;
      color: #ef4444;
    }

    /* Warning Toast */
    .toast-warning {
      border-left: 4px solid #f59e0b;
    }

    .toast-warning .toast-icon {
      background-color: #fef3c7;
      color: #f59e0b;
    }

    /* Info Toast */
    .toast-info {
      border-left: 4px solid #3b82f6;
    }

    .toast-info .toast-icon {
      background-color: #dbeafe;
      color: #3b82f6;
    }

    /* Responsive */
    @media (max-width: 640px) {
      .toast-container {
        right: 10px;
        left: 10px;
        max-width: calc(100% - 20px);
      }

      .toast {
        padding: 12px;
      }

      .toast-message {
        font-size: 13px;
      }
    }
  `],
  animations: [
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('300ms ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({ transform: 'translateX(100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class ToastNotificationComponent implements OnInit {
  notifications: Notification[] = [];

  constructor(private notificationService: NotificationService) {}

  ngOnInit() {
    this.notificationService.notifications$.subscribe(
      notifications => this.notifications = notifications
    );
  }

  close(id: number) {
    this.notificationService.remove(id);
  }
}

