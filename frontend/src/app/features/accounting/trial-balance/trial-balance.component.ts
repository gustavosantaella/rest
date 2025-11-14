import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AccountingService } from '../../../core/services/accounting.service';
import { NotificationService } from '../../../core/services/notification.service';
import { TrialBalance, AccountingPeriod, AccountType } from '../../../core/models/accounting.model';

@Component({
  selector: 'app-trial-balance',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Balance de Comprobación</h2>
          <p class="text-gray-600 mt-1">Resumen de movimientos y saldos por cuenta</p>
        </div>
        <button
          (click)="exportToExcel()"
          class="btn-secondary flex items-center space-x-2"
          [disabled]="!trialBalance || trialBalance.length === 0"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <span>Exportar</span>
        </button>
      </div>

      <!-- Filtros -->
      <div class="card">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Período
            </label>
            <select [(ngModel)]="selectedPeriodId" (ngModelChange)="loadTrialBalance()" class="input-field">
              <option [value]="null">Todos los períodos</option>
              <option *ngFor="let period of periods" [value]="period.id">
                {{ period.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Fecha Desde
            </label>
            <input
              type="date"
              [(ngModel)]="startDate"
              (ngModelChange)="loadTrialBalance()"
              class="input-field"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Fecha Hasta
            </label>
            <input
              type="date"
              [(ngModel)]="endDate"
              (ngModelChange)="loadTrialBalance()"
              class="input-field"
            />
          </div>
        </div>
      </div>

      <!-- Balance de Comprobación -->
      <div class="card">
        <div *ngIf="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p class="mt-2 text-gray-600">Generando balance de comprobación...</p>
        </div>

        <div *ngIf="!loading && trialBalance && trialBalance.length > 0">
          <!-- Totales -->
          <div class="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div class="grid grid-cols-4 gap-4">
              <div>
                <span class="text-sm text-gray-600">Total Débito:</span>
                <p class="text-xl font-bold text-green-600">{{ totalDebit | number:'1.2-2' }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Total Crédito:</span>
                <p class="text-xl font-bold text-red-600">{{ totalCredit | number:'1.2-2' }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Diferencia:</span>
                <p class="text-xl font-bold" [class.text-green-600]="difference === 0" [class.text-red-600]="difference !== 0">
                  {{ difference | number:'1.2-2' }}
                </p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Estado:</span>
                <p>
                  <span [class]="'badge ' + (difference === 0 ? 'badge-success' : 'badge-danger')">
                    {{ difference === 0 ? 'Balanceado' : 'Desbalanceado' }}
                  </span>
                </p>
              </div>
            </div>
          </div>

          <!-- Tabla -->
          <div class="table-container">
            <table class="table">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Cuenta</th>
                  <th>Tipo</th>
                  <th class="text-right">Saldo Inicial</th>
                  <th class="text-right">Débito</th>
                  <th class="text-right">Crédito</th>
                  <th class="text-right">Saldo Final Deudor</th>
                  <th class="text-right">Saldo Final Acreedor</th>
                </tr>
              </thead>
              <tbody>
                <tr *ngFor="let item of trialBalance" [class.bg-gray-50]="item.final_balance_debit === 0 && item.final_balance_credit === 0">
                  <td class="font-mono font-semibold">{{ item.account_code }}</td>
                  <td>{{ item.account_name }}</td>
                  <td>
                    <span [class]="'badge ' + getAccountTypeClass(item.account_type)">
                      {{ getAccountTypeLabel(item.account_type) }}
                    </span>
                  </td>
                  <td class="text-right">{{ item.initial_balance | number:'1.2-2' }}</td>
                  <td class="text-right text-green-600">{{ item.debit | number:'1.2-2' }}</td>
                  <td class="text-right text-red-600">{{ item.credit | number:'1.2-2' }}</td>
                  <td class="text-right font-semibold">{{ item.final_balance_debit | number:'1.2-2' }}</td>
                  <td class="text-right font-semibold">{{ item.final_balance_credit | number:'1.2-2' }}</td>
                </tr>
              </tbody>
              <tfoot class="bg-gray-100 font-bold">
                <tr>
                  <td colspan="3" class="text-right">TOTALES:</td>
                  <td class="text-right">{{ totalInitial | number:'1.2-2' }}</td>
                  <td class="text-right text-green-600">{{ totalDebit | number:'1.2-2' }}</td>
                  <td class="text-right text-red-600">{{ totalCredit | number:'1.2-2' }}</td>
                  <td class="text-right">{{ totalFinalDebit | number:'1.2-2' }}</td>
                  <td class="text-right">{{ totalFinalCredit | number:'1.2-2' }}</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>

        <div *ngIf="!loading && (!trialBalance || trialBalance.length === 0)" class="text-center py-8 text-gray-500">
          No hay datos para mostrar. Ajusta los filtros o crea asientos contables.
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
export class TrialBalanceComponent implements OnInit {
  private accountingService = inject(AccountingService);
  private notificationService = inject(NotificationService);

  trialBalance: TrialBalance[] = [];
  periods: AccountingPeriod[] = [];
  selectedPeriodId: number | null = null;
  startDate: string = '';
  endDate: string = '';
  loading = false;

  AccountType = AccountType;

  ngOnInit(): void {
    this.loadPeriods();
    this.loadTrialBalance();
  }

  loadPeriods(): void {
    this.accountingService.getPeriods().subscribe({
      next: (periods) => {
        this.periods = periods;
      }
    });
  }

  loadTrialBalance(): void {
    this.loading = true;
    this.accountingService.getTrialBalance(
      this.selectedPeriodId || undefined,
      this.startDate || undefined,
      this.endDate || undefined
    ).subscribe({
      next: (data) => {
        this.trialBalance = data;
        this.loading = false;
      },
      error: () => {
        this.notificationService.error('Error al generar balance de comprobación');
        this.loading = false;
      }
    });
  }

  get totalDebit(): number {
    return this.trialBalance.reduce((sum, item) => sum + item.debit, 0);
  }

  get totalCredit(): number {
    return this.trialBalance.reduce((sum, item) => sum + item.credit, 0);
  }

  get totalInitial(): number {
    return this.trialBalance.reduce((sum, item) => sum + item.initial_balance, 0);
  }

  get totalFinalDebit(): number {
    return this.trialBalance.reduce((sum, item) => sum + item.final_balance_debit, 0);
  }

  get totalFinalCredit(): number {
    return this.trialBalance.reduce((sum, item) => sum + item.final_balance_credit, 0);
  }

  get difference(): number {
    return this.totalDebit - this.totalCredit;
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

  exportToExcel(): void {
    // TODO: Implementar exportación a Excel
    this.notificationService.info('Funcionalidad de exportación próximamente');
  }
}

