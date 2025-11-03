import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfirmService, ConfirmOptions } from '../../../core/services/confirm.service';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="confirm-overlay" *ngIf="options" [@fadeIn] (click)="cancel()">
      <div class="confirm-dialog" [@slideIn] (click)="$event.stopPropagation()">
        <div class="confirm-header" [ngClass]="'confirm-' + options.type">
          <div class="confirm-icon">
            <span *ngIf="options.type === 'danger'">⚠</span>
            <span *ngIf="options.type === 'warning'">⚠</span>
            <span *ngIf="options.type === 'info'">ℹ</span>
          </div>
          <h3 class="confirm-title">{{ options.title }}</h3>
        </div>
        
        <div class="confirm-body">
          <p class="confirm-message">{{ options.message }}</p>
        </div>
        
        <div class="confirm-footer">
          <button 
            class="btn btn-cancel" 
            (click)="cancel()"
          >
            {{ options.cancelText }}
          </button>
          <button 
            class="btn btn-confirm"
            [ngClass]="'btn-' + options.type"
            (click)="confirm()"
          >
            {{ options.confirmText }}
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .confirm-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      padding: 20px;
    }

    .confirm-dialog {
      background: white;
      border-radius: 12px;
      max-width: 500px;
      width: 100%;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
      overflow: hidden;
    }

    .confirm-header {
      padding: 24px 24px 16px;
      display: flex;
      align-items: center;
      gap: 16px;
      border-bottom: 1px solid #e5e7eb;
    }

    .confirm-icon {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      flex-shrink: 0;
    }

    .confirm-danger .confirm-icon {
      background-color: #fee2e2;
      color: #dc2626;
    }

    .confirm-warning .confirm-icon {
      background-color: #fef3c7;
      color: #f59e0b;
    }

    .confirm-info .confirm-icon {
      background-color: #dbeafe;
      color: #3b82f6;
    }

    .confirm-title {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
      color: #111827;
    }

    .confirm-body {
      padding: 16px 24px 24px;
    }

    .confirm-message {
      margin: 0;
      font-size: 14px;
      line-height: 1.6;
      color: #6b7280;
    }

    .confirm-footer {
      padding: 16px 24px;
      background-color: #f9fafb;
      display: flex;
      justify-content: flex-end;
      gap: 12px;
    }

    .btn {
      padding: 10px 20px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      border: none;
      outline: none;
    }

    .btn:focus {
      outline: 2px solid transparent;
      outline-offset: 2px;
    }

    .btn-cancel {
      background-color: white;
      color: #374151;
      border: 1px solid #d1d5db;
    }

    .btn-cancel:hover {
      background-color: #f9fafb;
    }

    .btn-confirm {
      color: white;
    }

    .btn-danger {
      background-color: #dc2626;
    }

    .btn-danger:hover {
      background-color: #b91c1c;
    }

    .btn-warning {
      background-color: #f59e0b;
    }

    .btn-warning:hover {
      background-color: #d97706;
    }

    .btn-info {
      background-color: #3b82f6;
    }

    .btn-info:hover {
      background-color: #2563eb;
    }

    /* Responsive */
    @media (max-width: 640px) {
      .confirm-dialog {
        max-width: 100%;
      }

      .confirm-header {
        padding: 20px 16px 12px;
      }

      .confirm-icon {
        width: 40px;
        height: 40px;
        font-size: 20px;
      }

      .confirm-title {
        font-size: 18px;
      }

      .confirm-body {
        padding: 12px 16px 20px;
      }

      .confirm-footer {
        padding: 12px 16px;
        flex-direction: column-reverse;
      }

      .btn {
        width: 100%;
      }
    }
  `],
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('200ms ease-out', style({ opacity: 1 }))
      ]),
      transition(':leave', [
        animate('150ms ease-in', style({ opacity: 0 }))
      ])
    ]),
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'scale(0.9)', opacity: 0 }),
        animate('200ms ease-out', style({ transform: 'scale(1)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('150ms ease-in', style({ transform: 'scale(0.9)', opacity: 0 }))
      ])
    ])
  ]
})
export class ConfirmDialogComponent implements OnInit {
  options: ConfirmOptions | null = null;

  constructor(private confirmService: ConfirmService) {}

  ngOnInit() {
    this.confirmService.confirm$.subscribe(
      options => this.options = options
    );
  }

  confirm() {
    this.confirmService.resolve(true);
  }

  cancel() {
    this.confirmService.resolve(false);
  }
}

