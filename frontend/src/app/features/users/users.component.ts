import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../../core/services/user.service';
import { AuthService } from '../../core/services/auth.service';
import { AuthPermissionsService } from '../../core/services/auth-permissions.service';
import { NotificationService } from '../../core/services/notification.service';
import { ConfirmService } from '../../core/services/confirm.service';
import { RoleService } from '../../core/services/role.service';
import { User, UserRole, UserCreate } from '../../core/models/user.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';
import { UserRolesModalComponent } from '../../shared/components/user-roles-modal/user-roles-modal.component';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective, UserRolesModalComponent],
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {
  private userService = inject(UserService);
  private authService = inject(AuthService);
  private authPermissionsService = inject(AuthPermissionsService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);
  private roleService = inject(RoleService);
  
  users: User[] = [];
  currentUser: User | null = null;
  currentUser$ = this.authService.currentUser$; // Observable para template
  showModal = false;
  editingUser: User | null = null;
  userForm!: FormGroup;
  loading = true;
  
  // Roles
  showRolesModal = false;
  selectedUserForRoles: User | null = null;
  
  // Exponer UserRole para el template
  UserRole = UserRole;
  
  roleLabels: Record<UserRole, string> = {
    [UserRole.ADMIN]: 'Administrador',
    [UserRole.MANAGER]: 'Gerente',
    [UserRole.WAITER]: 'Mesero',
    [UserRole.CASHIER]: 'Cajero',
    [UserRole.CHEF]: 'Cocinero'
  };
  
  roleDescriptions: Record<UserRole, string> = {
    [UserRole.ADMIN]: 'Acceso total al sistema',
    [UserRole.MANAGER]: 'Gestión de inventario y personal',
    [UserRole.WAITER]: 'Gestión de órdenes y mesas',
    [UserRole.CASHIER]: 'Gestión de pagos',
    [UserRole.CHEF]: 'Ver órdenes de cocina'
  };
  
  constructor() {
    this.initForm();
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }
  
  ngOnInit(): void {
    this.loadUsers();
  }
  
  initForm(): void {
    this.userForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      full_name: ['', Validators.required],
      password: ['', Validators.required]
    });
  }
  
  loadUsers(): void {
    this.loading = true;
    this.userService.getUsers().subscribe({
      next: (users) => {
        this.users = users;
        this.loading = false;
      }
    });
  }
  
  openModal(user?: User): void {
    this.editingUser = user || null;
    
    if (user) {
      this.userForm.patchValue({
        username: user.username,
        email: user.email,
        full_name: user.full_name
      });
      this.userForm.get('password')?.clearValidators();
      this.userForm.get('password')?.updateValueAndValidity();
    } else {
      this.userForm.reset();
      this.userForm.get('password')?.setValidators(Validators.required);
      this.userForm.get('password')?.updateValueAndValidity();
    }
    
    this.showModal = true;
  }
  
  closeModal(): void {
    this.showModal = false;
    this.editingUser = null;
  }
  
  saveUser(): void {
    if (this.userForm.invalid) return;
    
    const userData: any = { ...this.userForm.value };
    
    // Asignar rol base por defecto (WAITER)
    // Los roles personalizados se asignarán después usando el botón 👥
    userData.role = UserRole.WAITER;
    
    // Si no hay password en edición, removerlo
    if (this.editingUser && !userData.password) {
      delete userData.password;
    }
    
    if (this.editingUser) {
      this.userService.updateUser(this.editingUser.id, userData).subscribe({
        next: () => {
          this.loadUsers();
          this.closeModal();
          this.notificationService.success('Usuario actualizado exitosamente');
        },
        error: (err) => {
          this.notificationService.error('Error al actualizar usuario: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    } else {
      this.userService.createUser(userData).subscribe({
        next: (newUser) => {
          this.loadUsers();
          this.closeModal();
          this.notificationService.success('Usuario creado exitosamente. Ahora puedes asignarle roles usando el botón 👥');
        },
        error: (err) => {
          this.notificationService.error('Error al crear usuario: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    }
  }
  
  toggleUserStatus(user: User): void {
    const update: any = { is_active: !user.is_active };
    this.userService.updateUser(user.id, update).subscribe({
      next: () => {
        this.loadUsers();
      }
    });
  }
  
  deleteUser(user: User): void {
    if (user.id === this.currentUser?.id) {
      this.notificationService.warning('No puedes eliminar tu propio usuario');
      return;
    }
    
    this.confirmService.confirmDelete(`${user.full_name} (${user.username})`).subscribe(confirmed => {
      if (confirmed) {
        this.userService.deleteUser(user.id).subscribe({
          next: () => {
            this.loadUsers();
            this.notificationService.success('Usuario eliminado exitosamente');
          },
          error: (err) => {
            this.notificationService.error('Error al eliminar usuario: ' + (err.error?.detail || 'Error desconocido'));
          }
        });
      }
    });
  }
  
  getRoleBadgeClass(role: UserRole): string {
    const classes: Record<UserRole, string> = {
      [UserRole.ADMIN]: 'badge-danger',
      [UserRole.MANAGER]: 'badge-warning',
      [UserRole.WAITER]: 'badge-info',
      [UserRole.CASHIER]: 'badge-success',
      [UserRole.CHEF]: 'bg-orange-100 text-orange-800'
    };
    return classes[role];
  }
  
  canManageUser(user: User): boolean {
    // Admin puede gestionar a todos
    if (this.currentUser?.role === UserRole.ADMIN) {
      return true;
    }
    
    // Manager puede gestionar a meseros, cajeros y cocineros
    if (this.currentUser?.role === UserRole.MANAGER) {
      return user.role === UserRole.WAITER || 
             user.role === UserRole.CASHIER || 
             user.role === UserRole.CHEF;
    }
    
    return false;
  }
  
  openRolesModal(user: User): void {
    this.selectedUserForRoles = user;
    this.showRolesModal = true;
  }
  
  closeRolesModal(): void {
    this.showRolesModal = false;
    this.selectedUserForRoles = null;
  }
  
  onRolesSaved(): void {
    this.loadUsers();  // Recargar usuarios para ver los roles actualizados
    this.notificationService.success('Roles asignados exitosamente');
  }
  
  // Métodos de verificación de permisos
  canViewUsers(): boolean {
    return this.authPermissionsService.hasPermission('users.view');
  }
  
  canCreateUsers(): boolean {
    return this.authPermissionsService.hasPermission('users.create');
  }
  
  canEditUsers(): boolean {
    return this.authPermissionsService.hasPermission('users.edit');
  }
  
  canDeleteUsers(): boolean {
    return this.authPermissionsService.hasPermission('users.delete');
  }
  
  canManageUserPermissions(): boolean {
    return this.authPermissionsService.hasPermission('users.manage_permissions');
  }
}

