import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();
  
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
          console.log('Token inválido detectado en interceptor');
          authService.logout();
        }
      }
      return throwError(() => error);
    })
  );
};

