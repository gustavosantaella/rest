import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
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
  private cdr = inject(ChangeDetectorRef);
  
  currentUser: User | null = null;
  businessName: string = 'Sistema de Gestión';
  businessInitials: string = 'SG';
  sidebarOpen = true;
  configDropdownOpen = false;
  
  constructor() {}
  
  ngOnInit(): void {
    // Suscribirse al usuario actual
    this.authService.currentUser$.subscribe(user => {
      console.log('👤 Layout - Usuario actualizado:', user);
      this.currentUser = user;
      // Marcar para verificar cambios (más seguro que detectChanges)
      this.cdr.markForCheck();
    });
    
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
  
  toggleConfigDropdown(): void {
    this.configDropdownOpen = !this.configDropdownOpen;
  }
  
  isAdmin(): boolean {
    const result = this.currentUser?.role === 'admin';
    console.log('🔒 isAdmin() ->', result, '| currentUser:', this.currentUser);
    return result;
  }
  
  isAdminOrManager(): boolean {
    const result = this.currentUser?.role === 'admin' || this.currentUser?.role === 'manager';
    console.log('🔒 isAdminOrManager() ->', result, '| currentUser:', this.currentUser);
    return result;
  }
  
  logout(): void {
    this.authService.logout();
  }
}

