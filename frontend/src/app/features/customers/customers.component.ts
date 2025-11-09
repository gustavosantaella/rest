import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CustomerService } from '../../core/services/customer.service';
import { NotificationService } from '../../core/services/notification.service';
import { ConfirmService } from '../../core/services/confirm.service';
import { Customer, CustomerCreate, CustomerUpdate } from '../../core/models/customer.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-customers',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective],
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.scss']
})
export class CustomersComponent implements OnInit {
  private customerService = inject(CustomerService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);
  
  customers: Customer[] = [];
  filteredCustomers: Customer[] = [];
  showModal = false;
  editingCustomer: Customer | null = null;
  customerForm!: FormGroup;
  loading = true;
  searchTerm = '';
  
  constructor() {
    this.initForm();
  }
  
  ngOnInit(): void {
    this.loadCustomers();
  }
  
  initForm(): void {
    this.customerForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: [''],
      dni: [''],
      telefono: [''],
      correo: ['', Validators.email]
    });
  }
  
  loadCustomers(): void {
    this.loading = true;
    this.customerService.getCustomers().subscribe({
      next: (customers) => {
        this.customers = customers;
        this.filteredCustomers = customers;
        this.loading = false;
      },
      error: (err) => {
        this.notificationService.error('Error al cargar clientes');
        this.loading = false;
      }
    });
  }
  
  filterCustomers(): void {
    const term = this.searchTerm.toLowerCase().trim();
    if (!term) {
      this.filteredCustomers = this.customers;
      return;
    }
    
    this.filteredCustomers = this.customers.filter(customer => 
      customer.nombre.toLowerCase().includes(term) ||
      customer.apellido?.toLowerCase().includes(term) ||
      customer.dni?.toLowerCase().includes(term) ||
      customer.telefono?.toLowerCase().includes(term) ||
      customer.correo?.toLowerCase().includes(term)
    );
  }
  
  openModal(customer?: Customer): void {
    this.editingCustomer = customer || null;
    
    if (customer) {
      this.customerForm.patchValue({
        nombre: customer.nombre,
        apellido: customer.apellido,
        dni: customer.dni,
        telefono: customer.telefono,
        correo: customer.correo
      });
    } else {
      this.customerForm.reset();
    }
    
    this.showModal = true;
  }
  
  closeModal(): void {
    this.showModal = false;
    this.editingCustomer = null;
    this.customerForm.reset();
  }
  
  saveCustomer(): void {
    if (this.customerForm.invalid) {
      this.notificationService.warning('Por favor completa los campos requeridos');
      return;
    }
    
    const customerData: CustomerCreate | CustomerUpdate = this.customerForm.value;
    
    if (this.editingCustomer) {
      this.customerService.updateCustomer(this.editingCustomer.id, customerData).subscribe({
        next: () => {
          this.loadCustomers();
          this.closeModal();
          this.notificationService.success('Cliente actualizado exitosamente');
        },
        error: (err) => {
          this.notificationService.error('Error al actualizar cliente: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    } else {
      this.customerService.createCustomer(customerData as CustomerCreate).subscribe({
        next: () => {
          this.loadCustomers();
          this.closeModal();
          this.notificationService.success('Cliente creado exitosamente');
        },
        error: (err) => {
          this.notificationService.error('Error al crear cliente: ' + (err.error?.detail || 'Error desconocido'));
        }
      });
    }
  }
  
  deleteCustomer(customer: Customer): void {
    const customerName = customer.apellido 
      ? `${customer.nombre} ${customer.apellido}` 
      : customer.nombre;
    
    this.confirmService.confirmDelete(customerName).subscribe(confirmed => {
      if (confirmed) {
        this.customerService.deleteCustomer(customer.id).subscribe({
          next: () => {
            this.loadCustomers();
            this.notificationService.success('Cliente eliminado exitosamente');
          },
          error: (err) => {
            this.notificationService.error('Error al eliminar cliente: ' + (err.error?.detail || 'Error desconocido'));
          }
        });
      }
    });
  }
  
  getCustomerInitials(customer: Customer): string {
    const firstInitial = customer.nombre.charAt(0).toUpperCase();
    const lastInitial = customer.apellido ? customer.apellido.charAt(0).toUpperCase() : '';
    return firstInitial + lastInitial;
  }
  
  getCustomerFullName(customer: Customer): string {
    return customer.apellido 
      ? `${customer.nombre} ${customer.apellido}` 
      : customer.nombre;
  }
  
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  }
}

