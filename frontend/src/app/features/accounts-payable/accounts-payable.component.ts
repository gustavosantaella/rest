import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AccountsPayableService } from '../../core/services/accounts-payable.service';
import { NotificationService } from '../../core/services/notification.service';
import { ConfirmService } from '../../core/services/confirm.service';
import { AccountPayable, AccountPayableCreate, AccountStatus, AccountPaymentCreate, AccountsSummary } from '../../core/models/accounts.model';

@Component({
  selector: 'app-accounts-payable',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './accounts-payable.component.html',
  styleUrls: ['./accounts-payable.component.scss']
})
export class AccountsPayableComponent implements OnInit {
  private accountsService = inject(AccountsPayableService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);
  
  accounts: AccountPayable[] = [];
  summary: AccountsSummary | null = null;
  showModal = false;
  showPaymentModal = false;
  editingAccount: AccountPayable | null = null;
  selectedAccount: AccountPayable | null = null;
  accountForm!: FormGroup;
  paymentForm!: FormGroup;
  loading = true;
  filterStatus = '';
  
  AccountStatus = AccountStatus;
  
  constructor() {
    this.initForms();
  }
  
  ngOnInit(): void {
    this.loadAccounts();
    this.loadSummary();
  }
  
  initForms(): void {
    this.accountForm = this.fb.group({
      supplier_name: ['', Validators.required],
      supplier_phone: [''],
      supplier_email: ['', Validators.email],
      invoice_number: [''],
      description: ['', Validators.required],
      amount: ['', [Validators.required, Validators.min(0.01)]],
      due_date: ['', Validators.required],
      notes: ['']
    });
    
    this.paymentForm = this.fb.group({
      amount: ['', [Validators.required, Validators.min(0.01)]],
      payment_method: [''],
      reference: [''],
      notes: ['']
    });
  }
  
  loadAccounts(): void {
    this.loading = true;
    this.accountsService.getAccountsPayable(this.filterStatus).subscribe({
      next: (accounts) => {
        this.accounts = accounts;
        this.loading = false;
      },
      error: (err) => {
        this.notificationService.error('Error al cargar cuentas');
        this.loading = false;
      }
    });
  }
  
  loadSummary(): void {
    this.accountsService.getSummary().subscribe({
      next: (summary) => this.summary = summary,
      error: (err) => console.error('Error cargando resumen:', err)
    });
  }
  
  openModal(account?: AccountPayable): void {
    this.editingAccount = account || null;
    if (account) {
      this.accountForm.patchValue(account);
    } else {
      this.accountForm.reset();
    }
    this.showModal = true;
  }
  
  closeModal(): void {
    this.showModal = false;
    this.editingAccount = null;
  }
  
  saveAccount(): void {
    if (this.accountForm.invalid) return;
    
    const accountData = this.accountForm.value;
    
    if (this.editingAccount) {
      this.accountsService.updateAccountPayable(this.editingAccount.id, accountData).subscribe({
        next: () => {
          this.loadAccounts();
          this.loadSummary();
          this.closeModal();
          this.notificationService.success('Cuenta actualizada exitosamente');
        },
        error: (err) => this.notificationService.error(err.error?.detail || 'Error al actualizar')
      });
    } else {
      this.accountsService.createAccountPayable(accountData).subscribe({
        next: () => {
          this.loadAccounts();
          this.loadSummary();
          this.closeModal();
          this.notificationService.success('Cuenta creada exitosamente');
        },
        error: (err) => this.notificationService.error(err.error?.detail || 'Error al crear')
      });
    }
  }
  
  deleteAccount(account: AccountPayable): void {
    this.confirmService.confirmDelete(`cuenta #${account.id}`).subscribe(confirmed => {
      if (confirmed) {
        this.accountsService.deleteAccountPayable(account.id).subscribe({
          next: () => {
            this.loadAccounts();
            this.loadSummary();
            this.notificationService.success('Cuenta eliminada exitosamente');
          },
          error: (err) => this.notificationService.error('Error al eliminar')
        });
      }
    });
  }
  
  openPaymentModal(account: AccountPayable): void {
    this.selectedAccount = account;
    this.paymentForm.reset();
    this.paymentForm.patchValue({ amount: account.amount_pending });
    this.showPaymentModal = true;
  }
  
  closePaymentModal(): void {
    this.showPaymentModal = false;
    this.selectedAccount = null;
  }
  
  addPayment(): void {
    if (this.paymentForm.invalid || !this.selectedAccount) return;
    
    const paymentData: AccountPaymentCreate = this.paymentForm.value;
    
    this.accountsService.addPayment(this.selectedAccount.id, paymentData).subscribe({
      next: () => {
        this.loadAccounts();
        this.loadSummary();
        this.closePaymentModal();
        this.notificationService.success('Pago registrado exitosamente');
      },
      error: (err) => this.notificationService.error(err.error?.detail || 'Error al registrar pago')
    });
  }
  
  getStatusClass(status: AccountStatus): string {
    const classes: Record<AccountStatus, string> = {
      [AccountStatus.PENDING]: 'badge-warning',
      [AccountStatus.PARTIAL]: 'badge-info',
      [AccountStatus.PAID]: 'badge-success',
      [AccountStatus.OVERDUE]: 'badge-danger'
    };
    return classes[status];
  }
  
  getStatusText(status: AccountStatus): string {
    const texts: Record<AccountStatus, string> = {
      [AccountStatus.PENDING]: 'Pendiente',
      [AccountStatus.PARTIAL]: 'Parcial',
      [AccountStatus.PAID]: 'Pagado',
      [AccountStatus.OVERDUE]: 'Vencido'
    };
    return texts[status];
  }
  
  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('es-ES');
  }
  
  isOverdue(due_date: string): boolean {
    return new Date(due_date) < new Date();
  }
}

