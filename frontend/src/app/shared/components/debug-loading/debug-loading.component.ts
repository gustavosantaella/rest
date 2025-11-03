import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingService } from '../../../core/services/loading.service';

@Component({
  selector: 'app-debug-loading',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="showDebug" class="fixed bottom-4 right-4 bg-black bg-opacity-80 text-white px-4 py-2 rounded-lg text-xs font-mono z-[10000]">
      <div class="flex items-center space-x-2">
        <div [class]="((loading$ | async) || false) ? 'w-2 h-2 bg-green-500 rounded-full animate-pulse' : 'w-2 h-2 bg-gray-500 rounded-full'"></div>
        <span>Loading: {{ ((loading$ | async) || false) ? 'ON' : 'OFF' }}</span>
      </div>
      <div class="mt-1">
        Requests: {{ loadingService.getRequestCount() }}
      </div>
      <button 
        *ngIf="((loading$ | async) || false)"
        (click)="reset()" 
        class="mt-2 bg-red-600 hover:bg-red-700 px-2 py-1 rounded text-xs w-full"
      >
        Reset Loader
      </button>
    </div>
  `
})
export class DebugLoadingComponent {
  loadingService = inject(LoadingService);
  loading$ = this.loadingService.loading$;
  
  // Cambiar a true para ver el debug
  showDebug = true; // ← ACTIVADO para debugging
  
  reset(): void {
    this.loadingService.reset();
  }
}

