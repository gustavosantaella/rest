import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-accounting',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="container mx-auto px-4 py-6">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Módulo Contable</h1>
        <p class="text-gray-600">Sistema contable profesional para gestión de tu negocio</p>
      </div>

      <!-- Navegación por pestañas -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="flex space-x-8" aria-label="Tabs">
          <a
            routerLink="chart-of-accounts"
            routerLinkActive="border-primary-500 text-primary-600"
            class="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap"
          >
            📊 Plan de Cuentas
          </a>
          <a
            routerLink="journal-entries"
            routerLinkActive="border-primary-500 text-primary-600"
            class="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap"
          >
            📝 Asientos Contables
          </a>
          <a
            routerLink="general-ledger"
            routerLinkActive="border-primary-500 text-primary-600"
            class="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap"
          >
            📖 Libro Mayor
          </a>
          <a
            routerLink="trial-balance"
            routerLinkActive="border-primary-500 text-primary-600"
            class="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap"
          >
            ⚖️ Balance de Comprobación
          </a>
          <a
            routerLink="financial-statements"
            routerLinkActive="border-primary-500 text-primary-600"
            class="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap"
          >
            📈 Estados Financieros
          </a>
          <a
            routerLink="periods"
            routerLinkActive="border-primary-500 text-primary-600"
            class="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap"
          >
            📅 Períodos Contables
          </a>
        </nav>
      </div>

      <!-- Contenido de las rutas hijas -->
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      width: 100%;
    }
  `]
})
export class AccountingComponent implements OnInit {
  ngOnInit(): void {
    // Componente principal de navegación
  }
}

