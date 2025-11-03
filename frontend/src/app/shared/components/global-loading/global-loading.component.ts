import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingService } from '../../../core/services/loading.service';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-global-loading',
  standalone: true,
  imports: [CommonModule, LoadingSpinnerComponent],
  template: `
    <app-loading-spinner 
      [show]="(loading$ | async) || false"
      [isOverlay]="true"
      size="lg"
      message="Procesando..."
    ></app-loading-spinner>
  `
})
export class GlobalLoadingComponent {
  private loadingService = inject(LoadingService);
  loading$ = this.loadingService.loading$;
}

