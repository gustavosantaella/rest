import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap, catchError, of, timeout } from 'rxjs';
import { User, LoginRequest, LoginResponse, RegisterRequest, RegisterResponse } from '../models/user.model';
import { environment } from '../../../environments/environment';
import { AuthPermissionsService } from './auth-permissions.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private authPermissionsService = inject(AuthPermissionsService);
  
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private readonly TOKEN_KEY = 'access_token';
  
  constructor() {
    this.loadCurrentUser();
  }
  
  login(credentials: LoginRequest): Observable<LoginResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    return this.http.post<LoginResponse>(`${environment.apiUrl}/auth/login`, formData)
      .pipe(
        tap(response => {
          this.setToken(response.access_token);
          this.loadCurrentUser();
          // Cargar permisos del usuario
          this.authPermissionsService.loadUserPermissions().subscribe();
        })
      );
  }

  register(data: RegisterRequest): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(`${environment.apiUrl}/auth/register`, data);
  }
  
  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    this.currentUserSubject.next(null);
    this.authPermissionsService.clearPermissions();
    this.router.navigate(['/login']);
  }
  
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }
  
  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }
  
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
  
  private loadCurrentUser(): void {
    const token = this.getToken();
    console.log('🔐 loadCurrentUser() - Token existe:', !!token);
    
    if (this.isAuthenticated()) {
      console.log('📡 Intentando cargar usuario desde:', `${environment.apiUrl}/users/me`);
      
      this.http.get<User>(`${environment.apiUrl}/users/me`)
        .pipe(
          timeout(10000), // Timeout de 10 segundos
          catchError((error: any) => {
            console.error('❌ Error al cargar usuario:', error);
            
            // Solo hacer logout si el token es inválido (401 o 403)
            if (error.status === 401 || error.status === 403) {
              console.log('🔐 Token inválido o expirado - Cerrando sesión');
              localStorage.removeItem(this.TOKEN_KEY);
              this.currentUserSubject.next(null);
              this.authPermissionsService.clearPermissions();
            } else if (error.status === 0 || error.name === 'TimeoutError') {
              // Error de red o backend no disponible
              console.warn('⚠️ Backend no disponible. Manteniendo sesión local.');
              console.warn('💡 Asegúrate de que el backend esté corriendo: python run.py');
            } else if (error.status >= 500) {
              // Error del servidor
              console.warn('⚠️ Error del servidor. Manteniendo sesión local.');
            } else {
              // Otros errores
              console.warn('⚠️ Error al cargar usuario:', error.status || 'Red no disponible');
            }
            return of(null);
          })
        )
        .subscribe({
          next: user => {
            console.log('✅ Usuario cargado:', user);
            if (user) {
              this.currentUserSubject.next(user);
              // Cargar permisos del usuario
              this.authPermissionsService.loadUserPermissions().subscribe({
                next: (perms) => console.log('✅ Permisos cargados:', perms.total_permissions),
                error: (err) => console.warn('⚠️ Error al cargar permisos:', err)
              });
            } else {
              console.warn('⚠️ Usuario es null - no se actualizará currentUserSubject');
            }
          }
        });
    } else {
      console.log('⚠️ No hay token - Usuario no autenticado');
    }
  }
  
  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }
}

