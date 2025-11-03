import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { AuthService } from '../../core/services/auth.service';
import { ConfigurationService } from '../../core/services/configuration.service';
import { User } from '../../core/models/user.model';
import { BusinessConfiguration } from '../../core/models/configuration.model';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {
  authService = inject(AuthService); // Exponer para usar en template
  private configService = inject(ConfigurationService);
  private titleService = inject(Title);
  
  currentUser: User | null = null;
  businessName: string = 'Sistema de Gestión';
  businessInitials: string = 'SG';
  sidebarOpen = true;
  
  constructor() {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }
  
  ngOnInit(): void {
    this.loadBusinessName();
  }
  
  loadBusinessName(): void {
    this.configService.getConfiguration().subscribe({
      next: (config) => {
        if (config && config.business_name) {
          this.businessName = config.business_name;
          this.businessInitials = this.getInitials(config.business_name);
          // Actualizar título de la pestaña del navegador
          this.titleService.setTitle(`${config.business_name} - Sistema de Gestión`);
        }
      },
      error: () => {
        // Si no hay configuración, mantener el nombre por defecto
        this.businessName = 'Sistema de Gestión';
        this.businessInitials = 'SG';
        this.titleService.setTitle('Sistema de Gestión - Restaurante');
      }
    });
  }
  
  getInitials(name: string): string {
    return name
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .substring(0, 2)
      .toUpperCase();
  }
  
  toggleSidebar(): void {
    this.sidebarOpen = !this.sidebarOpen;
  }
  
  logout(): void {
    this.authService.logout();
  }
}

