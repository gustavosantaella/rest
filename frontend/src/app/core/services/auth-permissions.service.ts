import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

export interface UserPermissionsInfo {
  user: string;
  role: string;
  custom_roles: Array<{id: number, name: string}>;
  permissions: string[];
  total_permissions: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthPermissionsService {
  private http = inject(HttpClient);
  private permissionsSubject = new BehaviorSubject<Set<string>>(new Set());
  private userRoleSubject = new BehaviorSubject<string>('');
  
  public permissions$ = this.permissionsSubject.asObservable();
  public userRole$ = this.userRoleSubject.asObservable();

  /**
   * Cargar permisos del usuario actual desde el backend
   */
  loadUserPermissions(): Observable<UserPermissionsInfo> {
    return this.http.get<UserPermissionsInfo>(`${environment.apiUrl}/profile/my-permissions`).pipe(
      tap(info => {
        this.permissionsSubject.next(new Set(info.permissions));
        this.userRoleSubject.next(info.role);
      })
    );
  }

  /**
   * Verificar si el usuario tiene un permiso específico
   */
  hasPermission(permissionCode: string): boolean {
    const role = this.userRoleSubject.value;
    
    // Administradores tienen todos los permisos
    if (role === 'admin') {
      return true;
    }
    
    return this.permissionsSubject.value.has(permissionCode);
  }

  /**
   * Verificar si el usuario tiene AL MENOS UNO de los permisos especificados
   */
  hasAnyPermission(permissionCodes: string[]): boolean {
    const role = this.userRoleSubject.value;
    
    // Administradores tienen todos los permisos
    if (role === 'admin') {
      return true;
    }
    
    const userPermissions = this.permissionsSubject.value;
    return permissionCodes.some(perm => userPermissions.has(perm));
  }

  /**
   * Verificar si el usuario tiene TODOS los permisos especificados
   */
  hasAllPermissions(permissionCodes: string[]): boolean {
    const role = this.userRoleSubject.value;
    
    // Administradores tienen todos los permisos
    if (role === 'admin') {
      return true;
    }
    
    const userPermissions = this.permissionsSubject.value;
    return permissionCodes.every(perm => userPermissions.has(perm));
  }

  /**
   * Verificar si es administrador
   */
  isAdmin(): boolean {
    return this.userRoleSubject.value === 'admin';
  }

  /**
   * Obtener todos los permisos del usuario
   */
  getAllPermissions(): string[] {
    return Array.from(this.permissionsSubject.value);
  }

  /**
   * Limpiar permisos (al cerrar sesión)
   */
  clearPermissions(): void {
    this.permissionsSubject.next(new Set());
    this.userRoleSubject.next('');
  }
}

