import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading-button',
  standalone: true,
  imports: [CommonModule],
  template: `
    <button 
      [type]="type"
      [disabled]="disabled || loading"
      [class]="buttonClass + ' ' + (disabled || loading ? 'opacity-50 cursor-not-allowed' : '')"
      (click)="handleClick($event)"
    >
      <span *ngIf="!loading" class="flex items-center justify-center">
        <ng-content></ng-content>
      </span>
      
      <span *ngIf="loading" class="flex items-center justify-center">
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ loadingText }}
      </span>
    </button>
  `,
  styles: []
})
export class LoadingButtonComponent {
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() loading: boolean = false;
  @Input() disabled: boolean = false;
  @Input() loadingText: string = 'Procesando...';
  @Input() buttonClass: string = 'btn-primary';
  @Output() clicked = new EventEmitter<Event>();
  
  handleClick(event: Event): void {
    if (!this.loading && !this.disabled) {
      this.clicked.emit(event);
    }
  }
}

