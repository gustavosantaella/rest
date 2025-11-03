import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserPermission, PermissionUpdate } from '../models/permission.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PermissionService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/permissions`;

  getUserPermissions(userId: number): Observable<UserPermission> {
    return this.http.get<UserPermission>(`${this.apiUrl}/${userId}`);
  }

  updateUserPermissions(userId: number, permissions: PermissionUpdate): Observable<UserPermission> {
    return this.http.put<UserPermission>(`${this.apiUrl}/${userId}`, permissions);
  }
}

