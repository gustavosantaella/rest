import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoadingService {
  private loadingSubject = new BehaviorSubject<boolean>(false);
  private requestCount = 0;
  
  public loading$: Observable<boolean> = this.loadingSubject.asObservable();
  
  show(): void {
    this.requestCount++;
    console.log('🔄 Loading show - Count:', this.requestCount);
    if (this.requestCount === 1) {
      this.loadingSubject.next(true);
    }
    
    // Timeout de seguridad: auto-hide después de 30 segundos
    setTimeout(() => {
      if (this.requestCount > 0 && this.isLoading()) {
        console.warn('⚠️ Loading timeout - Auto-reset después de 30s');
        this.reset();
      }
    }, 30000);
  }
  
  hide(): void {
    this.requestCount--;
    console.log('✅ Loading hide - Count:', this.requestCount);
    if (this.requestCount <= 0) {
      this.requestCount = 0;
      this.loadingSubject.next(false);
    }
  }
  
  reset(): void {
    console.warn('🔄 Loading reset - Forzando a 0');
    this.requestCount = 0;
    this.loadingSubject.next(false);
  }
  
  isLoading(): boolean {
    return this.loadingSubject.value;
  }
  
  getRequestCount(): number {
    return this.requestCount;
  }
}

