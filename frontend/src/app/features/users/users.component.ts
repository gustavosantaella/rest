import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../../core/services/user.service';
import { AuthService } from '../../core/services/auth.service';
import { User, UserRole, UserCreate } from '../../core/models/user.model';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {
  private userService = inject(UserService);
  private authService = inject(AuthService);
  private fb = inject(FormBuilder);
  
  users: User[] = [];
  currentUser: User | null = null;
  showModal = false;
  editingUser: User | null = null;
  userForm!: FormGroup;
  loading = true;
  
  userRoles = Object.values(UserRole);
  // Exponer UserRole para el template
  UserRole = UserRole;
  
  roleLabels: Record<UserRole, string> = {
    [UserRole.ADMIN]: 'Administrador',
    [UserRole.MANAGER]: 'Gerente',
    [UserRole.WAITER]: 'Mesero',
    [UserRole.CASHIER]: 'Cajero'
  };
  
  roleDescriptions: Record<UserRole, string> = {
    [UserRole.ADMIN]: 'Acceso total al sistema',
    [UserRole.MANAGER]: 'Gestión de inventario y personal',
    [UserRole.WAITER]: 'Gestión de órdenes y mesas',
    [UserRole.CASHIER]: 'Gestión de pagos'
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
      role: [UserRole.WAITER, Validators.required],
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
      this.userForm.patchValue(user);
      this.userForm.get('password')?.clearValidators();
      this.userForm.get('password')?.updateValueAndValidity();
    } else {
      this.userForm.reset({ role: UserRole.WAITER });
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
    
    const userData: any = this.userForm.value;
    
    // Si no hay password en edición, removerlo
    if (this.editingUser && !userData.password) {
      delete userData.password;
    }
    
    if (this.editingUser) {
      this.userService.updateUser(this.editingUser.id, userData).subscribe({
        next: () => {
          this.loadUsers();
          this.closeModal();
        },
        error: (err) => {
          alert('Error al actualizar usuario: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    } else {
      this.userService.createUser(userData).subscribe({
        next: () => {
          this.loadUsers();
          this.closeModal();
        },
        error: (err) => {
          alert('Error al crear usuario: ' + (err.error?.detail || 'Error desconocido'));
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
      alert('No puedes eliminar tu propio usuario');
      return;
    }
    
    if (confirm(`¿Estás seguro de eliminar al usuario "${user.username}"?`)) {
      this.userService.deleteUser(user.id).subscribe({
        next: () => {
          this.loadUsers();
        }
      });
    }
  }
  
  getRoleBadgeClass(role: UserRole): string {
    const classes: Record<UserRole, string> = {
      [UserRole.ADMIN]: 'badge-danger',
      [UserRole.MANAGER]: 'badge-warning',
      [UserRole.WAITER]: 'badge-info',
      [UserRole.CASHIER]: 'badge-success'
    };
    return classes[role];
  }
  
  canManageUser(user: User): boolean {
    // Admin puede gestionar a todos
    if (this.currentUser?.role === UserRole.ADMIN) {
      return true;
    }
    
    // Manager puede gestionar a meseros y cajeros
    if (this.currentUser?.role === UserRole.MANAGER) {
      return user.role === UserRole.WAITER || user.role === UserRole.CASHIER;
    }
    
    return false;
  }
}

