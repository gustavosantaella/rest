import { Component, EventEmitter, Input, Output, OnInit, OnChanges, SimpleChanges, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RoleService } from '../../../core/services/role.service';
import { NotificationService } from '../../../core/services/notification.service';
import { Role } from '../../../core/models/role.model';
import { User } from '../../../core/models/user.model';

@Component({
  selector: 'app-user-roles-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="modal-overlay" *ngIf="isOpen" (click)="close()">
      <div class="modal-container" (click)="$event.stopPropagation()">
        <div class="modal-header">
          <div class="header-content">
            <span class="icon">👥</span>
            <div>
              <h2>Asignar Roles</h2>
              <p class="user-info">{{ user?.full_name }} ({{ user?.username }})</p>
            </div>
          </div>
          <button class="close-btn" (click)="close()">×</button>
        </div>

        <div class="modal-body" *ngIf="!loading">
          <p class="description">
            Selecciona los roles que tendrá este usuario
          </p>

          <div class="roles-list">
            <label 
              *ngFor="let role of availableRoles" 
              class="role-card"
              [class.selected]="selectedRoleIds.has(role.id)"
            >
              <input
                type="checkbox"
                [checked]="selectedRoleIds.has(role.id)"
                (change)="toggleRole(role.id)"
                [disabled]="saving"
              />
              <div class="role-content">
                <div class="role-info">
                  <strong>{{ role.name }}</strong>
                  <span class="role-desc" *ngIf="role.description">{{ role.description }}</span>
                  <span class="permissions-count">{{ role.permissions.length }} permisos</span>
                </div>
                <div class="role-badges">
                  <span *ngFor="let perm of role.permissions.slice(0, 3)" class="permission-badge">
                    {{ perm.name }}
                  </span>
                  <span *ngIf="role.permissions.length > 3" class="more-badge">
                    +{{ role.permissions.length - 3 }}
                  </span>
                </div>
              </div>
            </label>
          </div>

          <div *ngIf="availableRoles.length === 0" class="empty-state">
            <p>No hay roles disponibles. Crea roles en la sección de Configuración primero.</p>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-cancel" (click)="close()" [disabled]="saving">
            Cancelar
          </button>
          <button type="button" class="btn btn-save" (click)="save()" [disabled]="saving">
            <span *ngIf="!saving">💾 Guardar</span>
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
      max-width: 700px;
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

    .icon {
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

    .roles-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .role-card {
      border: 2px solid #e5e7eb;
      border-radius: 8px;
      padding: 16px;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }

    .role-card:hover {
      border-color: #cbd5e1;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .role-card.selected {
      border-color: #3b82f6;
      background-color: #eff6ff;
    }

    .role-card input[type="checkbox"] {
      margin-top: 2px;
      flex-shrink: 0;
    }

    .role-content {
      flex: 1;
    }

    .role-info strong {
      display: block;
      font-size: 15px;
      color: #111827;
      margin-bottom: 4px;
    }

    .role-desc {
      display: block;
      font-size: 13px;
      color: #6b7280;
      margin-bottom: 8px;
    }

    .permissions-count {
      display: inline-block;
      font-size: 12px;
      color: #3b82f6;
      font-weight: 500;
    }

    .role-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 8px;
    }

    .permission-badge {
      font-size: 11px;
      padding: 3px 8px;
      background-color: #f3f4f6;
      color: #374151;
      border-radius: 4px;
    }

    .more-badge {
      font-size: 11px;
      padding: 3px 8px;
      background-color: #dbeafe;
      color: #3b82f6;
      border-radius: 4px;
      font-weight: 600;
    }

    .empty-state {
      text-align: center;
      padding: 40px 20px;
      color: #6b7280;
    }

    .modal-footer {
      padding: 16px 24px;
      border-top: 1px solid #e5e7eb;
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      background-color: #f9fafb;
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
  `]
})
export class UserRolesModalComponent implements OnInit, OnChanges {
  @Input() user: User | null = null;
  @Input() isOpen = false;
  @Output() closeModal = new EventEmitter<void>();
  @Output() rolesSaved = new EventEmitter<void>();

  private roleService = inject(RoleService);
  private notificationService = inject(NotificationService);

  availableRoles: Role[] = [];
  selectedRoleIds: Set<number> = new Set();
  loading = false;
  saving = false;

  ngOnInit() {
    if (this.isOpen) {
      this.loadRoles();
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['isOpen'] && this.isOpen && this.user) {
      this.loadRoles();
    }
  }

  loadRoles() {
    if (!this.user) return;

    this.loading = true;

    Promise.all([
      this.roleService.getRoles().toPromise(),
      this.roleService.getUserRoles(this.user.id).toPromise()
    ]).then(([allRoles, userRoles]) => {
      this.availableRoles = allRoles || [];
      const currentRoles = userRoles?.roles || [];
      this.selectedRoleIds = new Set(currentRoles.map(r => r.id));
      this.loading = false;
    }).catch(err => {
      this.notificationService.error('Error al cargar roles');
      this.loading = false;
    });
  }

  toggleRole(roleId: number) {
    if (this.selectedRoleIds.has(roleId)) {
      this.selectedRoleIds.delete(roleId);
    } else {
      this.selectedRoleIds.add(roleId);
    }
  }

  save() {
    if (!this.user) return;

    this.saving = true;

    const roleIds = Array.from(this.selectedRoleIds);

    this.roleService.updateUserRoles(this.user.id, { role_ids: roleIds }).subscribe({
      next: () => {
        this.saving = false;
        this.notificationService.success('Roles asignados exitosamente');
        this.rolesSaved.emit();
        this.close();
      },
      error: (err) => {
        this.saving = false;
        this.notificationService.error('Error al asignar roles: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }

  close() {
    this.closeModal.emit();
    this.selectedRoleIds.clear();
  }
}

