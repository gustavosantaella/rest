import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { finalize } from 'rxjs';
import { LoadingService } from '../services/loading.service';

export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loadingService = inject(LoadingService);
  
  // Mostrar loader
  loadingService.show();
  
  // Ocultar loader cuando termine (éxito o error)
  return next(req).pipe(
    finalize(() => {
      loadingService.hide();
    })
  );
};

