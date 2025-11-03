import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ConfigurationService } from '../../core/services/configuration.service';
import { UserService } from '../../core/services/user.service';
import { PaymentMethodService } from '../../core/services/payment-method.service';
import { BusinessConfiguration, Partner, BusinessConfigurationCreate, PartnerCreate } from '../../core/models/configuration.model';
import { User, UserRole } from '../../core/models/user.model';
import { PaymentMethod, PaymentMethodType, PaymentMethodCreate, PAYMENT_METHOD_LABELS } from '../../core/models/payment-method.model';
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
  private paymentMethodService = inject(PaymentMethodService);
  private fb = inject(FormBuilder);
  
  configuration: BusinessConfiguration | null = null;
  adminUsers: User[] = [];
  partners: Partner[] = [];
  paymentMethods: PaymentMethod[] = [];
  
  showPartnerModal = false;
  editingPartner: Partner | null = null;
  
  showPaymentMethodModal = false;
  editingPaymentMethod: PaymentMethod | null = null;
  selectedPaymentType: string = '';
  
  configForm!: FormGroup;
  partnerForm!: FormGroup;
  paymentMethodForm!: FormGroup;
  
  loading = true;
  configExists = false;
  
  PaymentMethodType = PaymentMethodType;
  
  constructor() {
    this.initForms();
  }
  
  ngOnInit(): void {
    this.loadData();
  }
  
  initForms(): void {
    this.configForm = this.fb.group({
      business_name: ['', Validators.required],
      slug: [''],
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
    
    this.paymentMethodForm = this.fb.group({
      type: ['', Validators.required],
      name: ['', Validators.required],
      phone: [''],
      dni: [''],
      bank: [''],
      account_holder: [''],
      account_number: [''],
      is_active: [true]
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
    
    // Cargar métodos de pago
    this.paymentMethodService.getPaymentMethods().subscribe({
      next: (methods) => {
        this.paymentMethods = methods;
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
  
  // Payment Methods
  openPaymentMethodModal(method?: PaymentMethod): void {
    this.editingPaymentMethod = method || null;
    
    if (method) {
      this.selectedPaymentType = method.type;
      this.paymentMethodForm.patchValue(method);
    } else {
      this.paymentMethodForm.reset({ is_active: true });
      this.selectedPaymentType = '';
    }
    
    this.showPaymentMethodModal = true;
  }
  
  closePaymentMethodModal(): void {
    this.showPaymentMethodModal = false;
    this.editingPaymentMethod = null;
    this.selectedPaymentType = '';
  }
  
  onPaymentTypeChange(): void {
    const type = this.paymentMethodForm.get('type')?.value;
    this.selectedPaymentType = type;
    
    // Limpiar campos
    this.paymentMethodForm.patchValue({
      phone: '',
      dni: '',
      bank: '',
      account_holder: '',
      account_number: ''
    });
    
    // Configurar validadores según tipo
    if (type === 'pago_movil') {
      this.setRequiredFields(['phone', 'dni', 'bank', 'account_holder']);
    } else if (type === 'transferencia') {
      this.setRequiredFields(['account_number', 'dni', 'bank', 'account_holder']);
    } else {
      this.clearRequiredFields();
    }
  }
  
  private setRequiredFields(fields: string[]): void {
    // Primero limpiar todos
    this.clearRequiredFields();
    // Luego establecer los requeridos
    fields.forEach(field => {
      this.paymentMethodForm.get(field)?.setValidators(Validators.required);
      this.paymentMethodForm.get(field)?.updateValueAndValidity();
    });
  }
  
  private clearRequiredFields(): void {
    ['phone', 'dni', 'bank', 'account_holder', 'account_number'].forEach(field => {
      this.paymentMethodForm.get(field)?.clearValidators();
      this.paymentMethodForm.get(field)?.updateValueAndValidity();
    });
  }
  
  savePaymentMethod(): void {
    if (this.paymentMethodForm.invalid) return;
    
    if (!this.configExists) {
      alert('Primero debes crear la configuración del negocio');
      return;
    }
    
    const data: PaymentMethodCreate = this.paymentMethodForm.value;
    
    if (this.editingPaymentMethod) {
      this.paymentMethodService.updatePaymentMethod(this.editingPaymentMethod.id, data).subscribe({
        next: () => {
          this.loadData();
          this.closePaymentMethodModal();
        },
        error: (err) => {
          alert('Error: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    } else {
      this.paymentMethodService.createPaymentMethod(data).subscribe({
        next: () => {
          this.loadData();
          this.closePaymentMethodModal();
        },
        error: (err) => {
          alert('Error: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    }
  }
  
  deletePaymentMethod(method: PaymentMethod): void {
    if (confirm(`¿Estás seguro de eliminar el método de pago "${method.name}"?`)) {
      this.paymentMethodService.deletePaymentMethod(method.id).subscribe({
        next: () => {
          this.loadData();
        }
      });
    }
  }
  
  getPaymentMethodLabel(type: string): string {
    return PAYMENT_METHOD_LABELS[type as PaymentMethodType] || type;
  }
  
  getPaymentMethodIcon(type: string): string {
    const icons: Record<string, string> = {
      'pago_movil': '💳',
      'transferencia': '🏦',
      'efectivo': '💵',
      'bolivares': 'Bs',
      'dolares': '$',
      'euros': '€'
    };
    return icons[type] || '💰';
  }
}

