import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ConfigurationService } from '../../core/services/configuration.service';
import { UserService } from '../../core/services/user.service';
import { BusinessConfiguration, Partner, BusinessConfigurationCreate, PartnerCreate } from '../../core/models/configuration.model';
import { User, UserRole } from '../../core/models/user.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-configuration',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective],
  templateUrl: './configuration.component.html',
  styleUrls: ['./configuration.component.scss']
})
export class ConfigurationComponent implements OnInit {
  private configService = inject(ConfigurationService);
  private userService = inject(UserService);
  private fb = inject(FormBuilder);
  
  configuration: BusinessConfiguration | null = null;
  adminUsers: User[] = [];
  partners: Partner[] = [];
  
  showPartnerModal = false;
  editingPartner: Partner | null = null;
  
  configForm!: FormGroup;
  partnerForm!: FormGroup;
  
  loading = true;
  configExists = false;
  
  constructor() {
    this.initForms();
  }
  
  ngOnInit(): void {
    this.loadData();
  }
  
  initForms(): void {
    this.configForm = this.fb.group({
      business_name: ['', Validators.required],
      legal_name: [''],
      rif: [''],
      phone: [''],
      email: ['', Validators.email],
      address: [''],
      tax_rate: [16, [Validators.required, Validators.min(0), Validators.max(100)]],
      currency: ['USD', Validators.required],
      logo_url: ['']
    });
    
    this.partnerForm = this.fb.group({
      user_id: ['', Validators.required],
      participation_percentage: [0, [Validators.required, Validators.min(0), Validators.max(100)]],
      investment_amount: [0, [Validators.min(0)]],
      is_active: [true],
      notes: ['']
    });
  }
  
  loadData(): void {
    this.loading = true;
    
    // Cargar configuración
    this.configService.getConfiguration().subscribe({
      next: (config) => {
        this.configuration = config;
        this.partners = config.partners;
        this.configForm.patchValue(config);
        this.configExists = true;
        this.loading = false;
      },
      error: (err) => {
        if (err.status === 404) {
          // No existe configuración aún
          this.configExists = false;
        }
        this.loading = false;
      }
    });
    
    // Cargar usuarios administradores
    this.userService.getUsers().subscribe({
      next: (users) => {
        this.adminUsers = users.filter(u => u.role === UserRole.ADMIN && u.is_active);
      }
    });
  }
  
  saveConfiguration(): void {
    if (this.configForm.invalid) return;
    
    const configData: BusinessConfigurationCreate = this.configForm.value;
    
    if (this.configExists) {
      // Actualizar
      this.configService.updateConfiguration(configData).subscribe({
        next: () => {
          this.loadData();
          alert('Configuración actualizada exitosamente. Recarga la página (F5) para ver el nombre actualizado.');
        },
        error: (err) => {
          alert('Error al actualizar: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    } else {
      // Crear
      this.configService.createConfiguration(configData).subscribe({
        next: () => {
          this.loadData();
          alert('Configuración creada exitosamente. Recarga la página (F5) para ver el nombre de tu negocio.');
        },
        error: (err) => {
          alert('Error al crear: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    }
  }
  
  // Partners
  openPartnerModal(partner?: Partner): void {
    this.editingPartner = partner || null;
    
    if (partner) {
      this.partnerForm.patchValue(partner);
    } else {
      this.partnerForm.reset({
        participation_percentage: 0,
        investment_amount: 0,
        is_active: true
      });
    }
    
    this.showPartnerModal = true;
  }
  
  closePartnerModal(): void {
    this.showPartnerModal = false;
    this.editingPartner = null;
  }
  
  savePartner(): void {
    if (this.partnerForm.invalid) return;
    
    if (!this.configExists) {
      alert('Primero debes crear la configuración del negocio');
      return;
    }
    
    const partnerData: PartnerCreate = this.partnerForm.value;
    
    if (this.editingPartner) {
      this.configService.updatePartner(this.editingPartner.id, partnerData).subscribe({
        next: () => {
          this.loadData();
          this.closePartnerModal();
        },
        error: (err) => {
          alert('Error: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    } else {
      this.configService.addPartner(partnerData).subscribe({
        next: () => {
          this.loadData();
          this.closePartnerModal();
        },
        error: (err) => {
          alert('Error: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    }
  }
  
  deletePartner(partner: Partner): void {
    if (confirm(`¿Estás seguro de eliminar a ${partner.user_name} como socio?`)) {
      this.configService.deletePartner(partner.id).subscribe({
        next: () => {
          this.loadData();
        }
      });
    }
  }
  
  getTotalParticipation(): number {
    return this.partners
      .filter(p => p.is_active)
      .reduce((sum, p) => sum + p.participation_percentage, 0);
  }
  
  getAvailableUsers(): User[] {
    const partnerUserIds = this.partners.map(p => p.user_id);
    return this.adminUsers.filter(u => !partnerUserIds.includes(u.id));
  }
}

