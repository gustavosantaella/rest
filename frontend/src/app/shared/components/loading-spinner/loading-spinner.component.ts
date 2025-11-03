import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading-spinner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div 
      *ngIf="show" 
      [class]="isOverlay ? 'loading-overlay' : 'loading-inline'"
      [ngClass]="customClass"
    >
      <div class="loading-spinner-container">
        <!-- Spinner -->
        <div [class]="spinnerSizeClass">
          <div class="spinner"></div>
        </div>
        
        <!-- Mensaje opcional -->
        <p *ngIf="message" class="loading-message">{{ message }}</p>
      </div>
    </div>
  `,
  styles: [`
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9998;
      animation: fadeIn 0.2s ease;
    }
    
    .loading-inline {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    
    .loading-spinner-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }
    
    .spinner-sm { width: 32px; height: 32px; }
    .spinner-md { width: 48px; height: 48px; }
    .spinner-lg { width: 64px; height: 64px; }
    .spinner-xl { width: 80px; height: 80px; }
    
    .spinner {
      width: 100%;
      height: 100%;
      border: 4px solid rgba(255, 255, 255, 0.3);
      border-top: 4px solid #fff;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    
    .loading-overlay .spinner {
      border: 4px solid rgba(255, 255, 255, 0.3);
      border-top: 4px solid #fff;
    }
    
    .loading-inline .spinner {
      border: 4px solid rgba(14, 165, 233, 0.3);
      border-top: 4px solid #0ea5e9;
    }
    
    .loading-message {
      color: white;
      font-size: 0.875rem;
      font-weight: 500;
      margin: 0;
      text-align: center;
    }
    
    .loading-inline .loading-message {
      color: #0ea5e9;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
  `]
})
export class LoadingSpinnerComponent {
  @Input() show: boolean = false;
  @Input() isOverlay: boolean = true;
  @Input() size: 'sm' | 'md' | 'lg' | 'xl' = 'md';
  @Input() message: string = '';
  @Input() customClass: string = '';
  
  get spinnerSizeClass(): string {
    return `spinner-${this.size}`;
  }
}

