import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

const TOKEN_KEY = 'access_token';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  
  // Obtener token directamente de localStorage para evitar dependencia circular
  const token = localStorage.getItem(TOKEN_KEY);
  
  // Agregar token si existe
  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  
  // Manejar respuestas de error
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      // Si recibimos 401 o 403, el token es inválido
      if (error.status === 401 || error.status === 403) {
        // Solo hacer logout si no estamos ya en login
        if (!req.url.includes('/auth/login')) {
          console.log('🔐 Token inválido detectado - Redirigiendo a login');
          // Limpiar token y redirigir sin inyectar AuthService (evita dependencia circular)
          localStorage.removeItem(TOKEN_KEY);
          router.navigate(['/login']);
        }
      } else if (error.status === 0) {
        // Error de red - no hacer logout
        console.warn('⚠️ Error de red detectado. Verifica que el backend esté corriendo en:', req.url);
      } else if (error.status >= 500) {
        // Error del servidor - no hacer logout
        console.error('⚠️ Error del servidor:', error.status);
      }
      return throwError(() => error);
    })
  );
};

