import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  Role, 
  RoleCreate, 
  RoleUpdate, 
  Permission,
  PermissionsByModule,
  UserRolesUpdate,
  UserRolesResponse
} from '../models/role.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RoleService {
  private http = inject(HttpClient);
  private rolesUrl = `${environment.apiUrl}/roles`;
  private permissionsUrl = `${environment.apiUrl}/system-permissions`;

  // Roles
  getRoles(): Observable<Role[]> {
    return this.http.get<Role[]>(this.rolesUrl);
  }

  getRole(id: number): Observable<Role> {
    return this.http.get<Role>(`${this.rolesUrl}/${id}`);
  }

  createRole(role: RoleCreate): Observable<Role> {
    return this.http.post<Role>(this.rolesUrl, role);
  }

  updateRole(id: number, role: RoleUpdate): Observable<Role> {
    return this.http.put<Role>(`${this.rolesUrl}/${id}`, role);
  }

  deleteRole(id: number): Observable<void> {
    return this.http.delete<void>(`${this.rolesUrl}/${id}`);
  }

  // Permisos del sistema
  getAllPermissions(): Observable<Permission[]> {
    return this.http.get<Permission[]>(this.permissionsUrl);
  }

  getPermissionsByModule(): Observable<PermissionsByModule> {
    return this.http.get<PermissionsByModule>(`${this.permissionsUrl}/by-module`);
  }

  // Roles de usuario
  getUserRoles(userId: number): Observable<UserRolesResponse> {
    return this.http.get<UserRolesResponse>(`${this.rolesUrl}/user/${userId}/roles`);
  }

  updateUserRoles(userId: number, roleIds: UserRolesUpdate): Observable<UserRolesResponse> {
    return this.http.put<UserRolesResponse>(`${this.rolesUrl}/user/${userId}/roles`, roleIds);
  }
}

