import { Component, EventEmitter, Input, Output, OnInit, OnChanges, SimpleChanges, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PermissionService } from '../../../core/services/permission.service';
import { NotificationService } from '../../../core/services/notification.service';
import { UserPermission, PERMISSION_MODULES, PermissionModule } from '../../../core/models/permission.model';
import { User } from '../../../core/models/user.model';

@Component({
  selector: 'app-user-permissions-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="modal-overlay" *ngIf="isOpen" (click)="close()">
      <div class="modal-container" (click)="$event.stopPropagation()">
        <div class="modal-header">
          <div class="header-content">
            <span class="lock-icon">🔒</span>
            <div>
              <h2>Permisos de Acceso</h2>
              <p class="user-info">{{ user?.full_name }} ({{ user?.username }})</p>
            </div>
          </div>
          <button class="close-btn" (click)="close()">×</button>
        </div>

        <div class="modal-body" *ngIf="permissions">
          <p class="description">
            Selecciona los módulos a los que este usuario tendrá acceso
          </p>

          <div class="permissions-grid">
            <div 
              *ngFor="let module of modules" 
              class="permission-card"
              [class.active]="permissions[module.key]"
            >
              <label class="permission-label">
                <input
                  type="checkbox"
                  [(ngModel)]="permissions[module.key]"
                  [disabled]="saving"
                />
                <div class="permission-content">
                  <div class="permission-icon">{{ module.icon }}</div>
                  <div class="permission-info">
                    <strong>{{ module.label }}</strong>
                    <span class="permission-desc">{{ module.description }}</span>
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-cancel" (click)="close()" [disabled]="saving">
            Cancelar
          </button>
          <button class="btn btn-save" (click)="save()" [disabled]="saving">
            <span *ngIf="!saving">💾 Guardar Permisos</span>
            <span *ngIf="saving">Guardando...</span>
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10001;
      padding: 20px;
    }

    .modal-container {
      background: white;
      border-radius: 12px;
      max-width: 800px;
      width: 100%;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
    }

    .modal-header {
      padding: 24px;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .header-content {
      display: flex;
      gap: 16px;
      align-items: center;
    }

    .lock-icon {
      font-size: 32px;
    }

    .modal-header h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
      color: #111827;
    }

    .user-info {
      margin: 4px 0 0 0;
      font-size: 14px;
      color: #6b7280;
    }

    .close-btn {
      background: none;
      border: none;
      font-size: 28px;
      color: #9ca3af;
      cursor: pointer;
      padding: 0;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      transition: all 0.2s;
    }

    .close-btn:hover {
      background-color: #f3f4f6;
      color: #374151;
    }

    .modal-body {
      padding: 24px;
      overflow-y: auto;
      flex: 1;
    }

    .description {
      margin: 0 0 20px 0;
      color: #6b7280;
      font-size: 14px;
    }

    .permissions-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 12px;
    }

    .permission-card {
      border: 2px solid #e5e7eb;
      border-radius: 8px;
      transition: all 0.2s;
      background: white;
    }

    .permission-card:hover {
      border-color: #cbd5e1;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .permission-card.active {
      border-color: #3b82f6;
      background-color: #eff6ff;
    }

    .permission-label {
      display: block;
      padding: 16px;
      cursor: pointer;
      margin: 0;
    }

    .permission-label input[type="checkbox"] {
      display: none;
    }

    .permission-content {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .permission-icon {
      font-size: 24px;
      flex-shrink: 0;
    }

    .permission-info {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .permission-info strong {
      font-size: 14px;
      color: #111827;
      font-weight: 600;
    }

    .permission-desc {
      font-size: 12px;
      color: #6b7280;
    }

    .modal-footer {
      padding: 16px 24px;
      border-top: 1px solid #e5e7eb;
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      background-color: #f9fafb;
      border-bottom-left-radius: 12px;
      border-bottom-right-radius: 12px;
    }

    .btn {
      padding: 10px 20px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      border: none;
    }

    .btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .btn-cancel {
      background-color: white;
      color: #374151;
      border: 1px solid #d1d5db;
    }

    .btn-cancel:hover:not(:disabled) {
      background-color: #f9fafb;
    }

    .btn-save {
      background-color: #3b82f6;
      color: white;
    }

    .btn-save:hover:not(:disabled) {
      background-color: #2563eb;
    }

    @media (max-width: 768px) {
      .permissions-grid {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class UserPermissionsModalComponent implements OnInit, OnChanges {
  @Input() user: User | null = null;
  @Input() isOpen = false;
  @Output() closeModal = new EventEmitter<void>();
  @Output() permissionsSaved = new EventEmitter<void>();

  private permissionService = inject(PermissionService);
  private notificationService = inject(NotificationService);

  permissions: UserPermission | null = null;
  modules = PERMISSION_MODULES;
  saving = false;

  ngOnInit() {
    if (this.user && this.isOpen) {
      this.loadPermissions();
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isOpen'] && this.isOpen && this.user && !this.permissions) {
      this.loadPermissions();
    }
  }

  loadPermissions() {
    if (!this.user) return;

    this.permissionService.getUserPermissions(this.user.id).subscribe({
      next: (permissions) => {
        this.permissions = permissions;
      },
      error: (err) => {
        this.notificationService.error('Error al cargar permisos: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }

  save() {
    if (!this.user || !this.permissions) return;

    this.saving = true;

    const update = {
      can_access_dashboard: this.permissions.can_access_dashboard,
      can_access_inventory: this.permissions.can_access_inventory,
      can_access_products: this.permissions.can_access_products,
      can_access_menu: this.permissions.can_access_menu,
      can_access_tables: this.permissions.can_access_tables,
      can_access_orders: this.permissions.can_access_orders,
      can_access_users: this.permissions.can_access_users,
      can_access_configuration: this.permissions.can_access_configuration,
      can_access_reports: this.permissions.can_access_reports
    };

    this.permissionService.updateUserPermissions(this.user.id, update).subscribe({
      next: () => {
        this.saving = false;
        this.notificationService.success('Permisos actualizados exitosamente');
        this.permissionsSaved.emit();
        this.close();
      },
      error: (err) => {
        this.saving = false;
        this.notificationService.error('Error al actualizar permisos: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }

  close() {
    this.closeModal.emit();
    this.permissions = null;
  }
}

