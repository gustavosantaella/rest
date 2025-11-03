import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { GlobalLoadingComponent } from './shared/components/global-loading/global-loading.component';
import { DebugLoadingComponent } from './shared/components/debug-loading/debug-loading.component';
import { ToastNotificationComponent } from './shared/components/toast-notification/toast-notification.component';
import { ConfirmDialogComponent } from './shared/components/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet, 
    GlobalLoadingComponent, 
    DebugLoadingComponent, 
    ToastNotificationComponent,
    ConfirmDialogComponent
  ],
  template: `
    <router-outlet></router-outlet>
    <app-global-loading></app-global-loading>
    <app-debug-loading></app-debug-loading>
    <app-toast-notification></app-toast-notification>
    <app-confirm-dialog></app-confirm-dialog>
  `,
  styles: []
})
export class AppComponent {
  title = 'Sistema de Gestión - Restaurante';
}

