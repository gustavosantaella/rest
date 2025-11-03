import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { finalize, timeout, catchError, throwError } from 'rxjs';
import { LoadingService } from '../services/loading.service';

export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loadingService = inject(LoadingService);
  
  // No mostrar loader para la petición inicial de verificación de usuario
  // Esto evita el loader al cargar la app cuando el backend no está disponible
  const isInitialUserCheck = req.url.includes('/users/me');
  
  if (!isInitialUserCheck) {
    loadingService.show();
  }
  
  // Ocultar loader cuando termine (éxito o error) con timeout de seguridad
  return next(req).pipe(
    timeout(30000), // Timeout de 30 segundos como seguridad
    catchError((error) => {
      // Asegurar que hide() se llama incluso en error
      if (!isInitialUserCheck) {
        loadingService.hide();
      }
      return throwError(() => error);
    }),
    finalize(() => {
      if (!isInitialUserCheck) {
        loadingService.hide();
      }
    })
  );
};

