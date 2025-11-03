import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { GlobalLoadingComponent } from './shared/components/global-loading/global-loading.component';
import { DebugLoadingComponent } from './shared/components/debug-loading/debug-loading.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, GlobalLoadingComponent, DebugLoadingComponent],
  template: `
    <router-outlet></router-outlet>
    <app-global-loading></app-global-loading>
    <app-debug-loading></app-debug-loading>
  `,
  styles: []
})
export class AppComponent {
  title = 'Sistema de Gestión - Restaurante';
}

