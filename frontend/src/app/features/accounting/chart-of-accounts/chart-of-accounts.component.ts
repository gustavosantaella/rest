import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AccountingService } from '../../../core/services/accounting.service';
import { NotificationService } from '../../../core/services/notification.service';
import { ConfirmService } from '../../../core/services/confirm.service';
import { ChartOfAccounts, ChartOfAccountsCreate, AccountType, AccountNature } from '../../../core/models/accounting.model';
import { TooltipDirective } from '../../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-chart-of-accounts',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Plan de Cuentas</h2>
          <p class="text-gray-600 mt-1">Gestiona tu catálogo de cuentas contables</p>
        </div>
        <button
          (click)="openModal()"
          class="btn-primary flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <span>Nueva Cuenta</span>
        </button>
      </div>

      <!-- Filtros -->
      <div class="card">
        <div class="flex items-center space-x-4">
          <div class="flex-1">
            <input
              type="text"
              [(ngModel)]="searchTerm"
              (ngModelChange)="filterAccounts()"
              placeholder="Buscar por código o nombre..."
              class="input-field"
            />
          </div>
          <div>
            <select [(ngModel)]="filterType" (ngModelChange)="filterAccounts()" class="input-field">
              <option value="">Todos los tipos</option>
              <option [value]="AccountType.ASSET">Activo</option>
              <option [value]="AccountType.LIABILITY">Pasivo</option>
              <option [value]="AccountType.EQUITY">Patrimonio</option>
              <option [value]="AccountType.REVENUE">Ingreso</option>
              <option [value]="AccountType.EXPENSE">Gasto</option>
              <option [value]="AccountType.COST_OF_SALES">Costo de Ventas</option>
            </select>
          </div>
          <div>
            <label class="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                [(ngModel)]="showInactive"
                (ngModelChange)="loadAccounts()"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span class="text-sm text-gray-700">Mostrar inactivas</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Tabla de Cuentas -->
      <div class="card">
        <div *ngIf="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p class="mt-2 text-gray-600">Cargando cuentas...</p>
        </div>

        <div *ngIf="!loading && filteredAccounts.length === 0" class="text-center py-8 text-gray-500">
          No hay cuentas registradas
        </div>

        <div *ngIf="!loading && filteredAccounts.length > 0" class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Naturaleza</th>
                <th>Saldo Inicial</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let account of filteredAccounts" [class.bg-gray-50]="!account.is_active">
                <td class="font-mono font-semibold">{{ account.code }}</td>
                <td>
                  <div>
                    <p class="font-medium">{{ account.name }}</p>
                    <p *ngIf="account.description" class="text-xs text-gray-500">{{ account.description }}</p>
                  </div>
                </td>
                <td>
                  <span [class]="'badge ' + getAccountTypeClass(account.account_type)">
                    {{ getAccountTypeLabel(account.account_type) }}
                  </span>
                </td>
                <td>
                  <span [class]="'badge ' + (account.nature === AccountNature.DEBIT ? 'badge-info' : 'badge-warning')">
                    {{ account.nature === AccountNature.DEBIT ? 'Deudora' : 'Acreedora' }}
                  </span>
                </td>
                <td class="text-right font-semibold">
                  {{ account.initial_balance | number:'1.2-2' }}
                </td>
                <td>
                  <span [class]="'badge ' + (account.is_active ? 'badge-success' : 'badge-secondary')">
                    {{ account.is_active ? 'Activa' : 'Inactiva' }}
                  </span>
                </td>
                <td>
                  <div class="flex gap-2">
                    <button
                      (click)="openModal(account)"
                      class="btn-secondary text-sm py-1 px-3"
                      [disabled]="account.is_system"
                      title="Editar cuenta"
                    >
                      ✏️
                    </button>
                    <button
                      (click)="deleteAccount(account)"
                      class="btn-danger text-sm py-1 px-3"
                      [disabled]="account.is_system"
                      title="Eliminar cuenta"
                    >
                      🗑️
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Cuenta -->
    <div
      *ngIf="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      (click)="closeModal()"
    >
      <div
        class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        (click)="$event.stopPropagation()"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-gray-900">
              {{ editingAccount ? 'Editar Cuenta' : 'Nueva Cuenta' }}
            </h3>
            <button (click)="closeModal()" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <form [formGroup]="accountForm" (ngSubmit)="saveAccount()">
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Código *
                  </label>
                  <input
                    type="text"
                    formControlName="code"
                    class="input-field"
                    placeholder="Ej: 1.01.01.001"
                    appTooltip="Código único de la cuenta (ej: 1.01.01.001)"
                    tooltipPosition="top"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Nombre *
                  </label>
                  <input
                    type="text"
                    formControlName="name"
                    class="input-field"
                    placeholder="Nombre de la cuenta"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Descripción
                </label>
                <textarea
                  formControlName="description"
                  rows="2"
                  class="input-field"
                  placeholder="Descripción de la cuenta"
                ></textarea>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Tipo de Cuenta *
                  </label>
                  <select formControlName="account_type" class="input-field">
                    <option [value]="AccountType.ASSET">Activo</option>
                    <option [value]="AccountType.LIABILITY">Pasivo</option>
                    <option [value]="AccountType.EQUITY">Patrimonio</option>
                    <option [value]="AccountType.REVENUE">Ingreso</option>
                    <option [value]="AccountType.EXPENSE">Gasto</option>
                    <option [value]="AccountType.COST_OF_SALES">Costo de Ventas</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Naturaleza *
                  </label>
                  <select formControlName="nature" class="input-field">
                    <option [value]="AccountNature.DEBIT">Deudora</option>
                    <option [value]="AccountNature.CREDIT">Acreedora</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Saldo Inicial
                  </label>
                  <input
                    type="number"
                    formControlName="initial_balance"
                    step="0.01"
                    class="input-field"
                    placeholder="0.00"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Fecha Saldo Inicial
                  </label>
                  <input
                    type="date"
                    formControlName="initial_balance_date"
                    class="input-field"
                  />
                </div>
              </div>

              <div class="flex items-center space-x-4">
                <label class="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    formControlName="allows_manual_entries"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="text-sm text-gray-700">Permite asientos manuales</span>
                </label>

                <label class="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    formControlName="is_active"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="text-sm text-gray-700">Activa</span>
                </label>
              </div>
            </div>

            <div class="mt-6 flex justify-end space-x-3">
              <button type="button" (click)="closeModal()" class="btn-secondary">
                Cancelar
              </button>
              <button type="submit" [disabled]="accountForm.invalid" class="btn-primary">
                {{ editingAccount ? 'Actualizar' : 'Crear' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      width: 100%;
    }
  `]
})
export class ChartOfAccountsComponent implements OnInit {
  private accountingService = inject(AccountingService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);

  accounts: ChartOfAccounts[] = [];
  filteredAccounts: ChartOfAccounts[] = [];
  loading = true;
  showModal = false;
  editingAccount: ChartOfAccounts | null = null;
  searchTerm = '';
  filterType = '';
  showInactive = false;

  AccountType = AccountType;
  AccountNature = AccountNature;

  accountForm!: FormGroup;

  ngOnInit(): void {
    this.initForm();
    this.loadAccounts();
  }

  initForm(): void {
    this.accountForm = this.fb.group({
      code: ['', Validators.required],
      name: ['', Validators.required],
      description: [''],
      account_type: [AccountType.ASSET, Validators.required],
      nature: [AccountNature.DEBIT, Validators.required],
      parent_id: [null],
      level: [1],
      allows_manual_entries: [true],
      is_active: [true],
      initial_balance: [0],
      initial_balance_date: [null]
    });
  }

  loadAccounts(): void {
    this.loading = true;
    this.accountingService.getChartOfAccounts(!this.showInactive).subscribe({
      next: (accounts) => {
        this.accounts = accounts;
        this.filterAccounts();
        this.loading = false;
      },
      error: (err) => {
        this.notificationService.error('Error al cargar cuentas');
        this.loading = false;
      }
    });
  }

  filterAccounts(): void {
    this.filteredAccounts = this.accounts.filter(account => {
      const matchesSearch = !this.searchTerm ||
        account.code.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        account.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      
      const matchesType = !this.filterType || account.account_type === this.filterType;
      
      return matchesSearch && matchesType;
    });
  }

  openModal(account?: ChartOfAccounts): void {
    this.editingAccount = account || null;
    if (account) {
      this.accountForm.patchValue({
        code: account.code,
        name: account.name,
        description: account.description || '',
        account_type: account.account_type,
        nature: account.nature,
        parent_id: account.parent_id,
        level: account.level,
        allows_manual_entries: account.allows_manual_entries,
        is_active: account.is_active,
        initial_balance: account.initial_balance,
        initial_balance_date: account.initial_balance_date || null
      });
    } else {
      this.accountForm.reset({
        account_type: AccountType.ASSET,
        nature: AccountNature.DEBIT,
        allows_manual_entries: true,
        is_active: true,
        initial_balance: 0
      });
    }
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.editingAccount = null;
    this.accountForm.reset();
  }

  saveAccount(): void {
    if (this.accountForm.invalid) return;

    const accountData: ChartOfAccountsCreate = this.accountForm.value;

    if (this.editingAccount) {
      this.accountingService.updateAccount(this.editingAccount.id, accountData).subscribe({
        next: () => {
          this.notificationService.success('Cuenta actualizada exitosamente');
          this.loadAccounts();
          this.closeModal();
        },
        error: (err) => {
          this.notificationService.error(err.error?.detail || 'Error al actualizar cuenta');
        }
      });
    } else {
      this.accountingService.createAccount(accountData).subscribe({
        next: () => {
          this.notificationService.success('Cuenta creada exitosamente');
          this.loadAccounts();
          this.closeModal();
        },
        error: (err) => {
          this.notificationService.error(err.error?.detail || 'Error al crear cuenta');
        }
      });
    }
  }

  deleteAccount(account: ChartOfAccounts): void {
    if (account.is_system) {
      this.notificationService.warning('No se puede eliminar una cuenta del sistema');
      return;
    }

    this.confirmService.confirmDelete(`cuenta ${account.code} - ${account.name}`).subscribe(confirmed => {
      if (confirmed) {
        this.accountingService.deleteAccount(account.id).subscribe({
          next: () => {
            this.notificationService.success('Cuenta eliminada exitosamente');
            this.loadAccounts();
          },
          error: (err) => {
            this.notificationService.error(err.error?.detail || 'Error al eliminar cuenta');
          }
        });
      }
    });
  }

  getAccountTypeLabel(type: AccountType): string {
    const labels: Record<AccountType, string> = {
      [AccountType.ASSET]: 'Activo',
      [AccountType.LIABILITY]: 'Pasivo',
      [AccountType.EQUITY]: 'Patrimonio',
      [AccountType.REVENUE]: 'Ingreso',
      [AccountType.EXPENSE]: 'Gasto',
      [AccountType.COST_OF_SALES]: 'Costo de Ventas'
    };
    return labels[type] || type;
  }

  getAccountTypeClass(type: AccountType): string {
    const classes: Record<AccountType, string> = {
      [AccountType.ASSET]: 'badge-info',
      [AccountType.LIABILITY]: 'badge-warning',
      [AccountType.EQUITY]: 'badge-success',
      [AccountType.REVENUE]: 'badge-primary',
      [AccountType.EXPENSE]: 'badge-danger',
      [AccountType.COST_OF_SALES]: 'badge-secondary'
    };
    return classes[type] || 'badge-secondary';
  }
}

