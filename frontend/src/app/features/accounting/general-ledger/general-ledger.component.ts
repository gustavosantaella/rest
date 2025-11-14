import { Component, OnInit, inject } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { AccountingService } from "../../../core/services/accounting.service";
import { NotificationService } from "../../../core/services/notification.service";
import {
  ChartOfAccounts,
  GeneralLedger,
  AccountingPeriod,
} from "../../../core/models/accounting.model";

@Component({
  selector: "app-general-ledger",
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Libro Mayor</h2>
        <p class="text-gray-600 mt-1">
          Consulta los movimientos contables por cuenta
        </p>
      </div>

      <!-- Filtros -->
      <div class="card">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Cuenta *
            </label>
            <select
              [(ngModel)]="selectedAccountId"
              (ngModelChange)="loadLedger()"
              class="input-field"
            >
              <option [value]="null">Seleccionar cuenta</option>
              <option *ngFor="let account of accounts" [value]="account.id">
                {{ account.code }} - {{ account.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Período
            </label>
            <select
              [(ngModel)]="selectedPeriodId"
              (ngModelChange)="loadLedger()"
              class="input-field"
            >
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
              (ngModelChange)="loadLedger()"
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
              (ngModelChange)="loadLedger()"
              class="input-field"
            />
          </div>
        </div>
      </div>

      <!-- Libro Mayor -->
      <div class="card" *ngIf="selectedAccountId">
        <div *ngIf="loading" class="text-center py-8">
          <div
            class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"
          ></div>
          <p class="mt-2 text-gray-600">Cargando libro mayor...</p>
        </div>

        <div
          *ngIf="!loading && ledgerEntries.length === 0"
          class="text-center py-8 text-gray-500"
        >
          No hay movimientos para esta cuenta en el período seleccionado
        </div>

        <div *ngIf="!loading && ledgerEntries.length > 0">
          <!-- Resumen -->
          <div class="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div class="grid grid-cols-4 gap-4">
              <div>
                <span class="text-sm text-gray-600">Cuenta:</span>
                <p class="font-bold">
                  {{ selectedAccount?.code }} - {{ selectedAccount?.name }}
                </p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Total Débito:</span>
                <p class="font-bold text-green-600">
                  {{ totalDebit | number : "1.2-2" }}
                </p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Total Crédito:</span>
                <p class="font-bold text-red-600">
                  {{ totalCredit | number : "1.2-2" }}
                </p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Saldo Final:</span>
                <p
                  class="font-bold"
                  [class.text-green-600]="finalBalance >= 0"
                  [class.text-red-600]="finalBalance < 0"
                >
                  {{ finalBalance | number : "1.2-2" }}
                </p>
              </div>
            </div>
          </div>

          <!-- Tabla de Movimientos -->
          <div class="table-container">
            <table class="table">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Asiento</th>
                  <th>Descripción</th>
                  <th>Referencia</th>
                  <th class="text-right">Débito</th>
                  <th class="text-right">Crédito</th>
                  <th class="text-right">Saldo Deudor</th>
                  <th class="text-right">Saldo Acreedor</th>
                </tr>
              </thead>
              <tbody>
                <tr *ngFor="let entry of ledgerEntries">
                  <td>{{ entry.entry_date | date : "short" }}</td>
                  <td class="font-mono">{{ entry.entry_number }}</td>
                  <td>{{ entry.description || "-" }}</td>
                  <td>{{ entry.reference || "-" }}</td>
                  <td class="text-right text-green-600">
                    {{ entry.debit | number : "1.2-2" }}
                  </td>
                  <td class="text-right text-red-600">
                    {{ entry.credit | number : "1.2-2" }}
                  </td>
                  <td class="text-right">
                    {{ entry.balance_debit | number : "1.2-2" }}
                  </td>
                  <td class="text-right">
                    {{ entry.balance_credit | number : "1.2-2" }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div *ngIf="!selectedAccountId" class="card">
        <div class="text-center py-8 text-gray-500">
          Selecciona una cuenta para ver su libro mayor
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
        width: 100%;
      }
    `,
  ],
})
export class GeneralLedgerComponent implements OnInit {
  private accountingService = inject(AccountingService);
  private notificationService = inject(NotificationService);

  accounts: ChartOfAccounts[] = [];
  periods: AccountingPeriod[] = [];
  ledgerEntries: GeneralLedger[] = [];
  selectedAccount: ChartOfAccounts | null = null;
  selectedAccountId: number | null = null;
  selectedPeriodId: number | null = null;
  startDate: string = "";
  endDate: string = "";
  loading = false;

  get totalDebit(): number {
    return this.ledgerEntries.reduce((sum, entry) => sum + entry.debit, 0);
  }

  get totalCredit(): number {
    return this.ledgerEntries.reduce((sum, entry) => sum + entry.credit, 0);
  }

  get finalBalance(): number {
    if (!this.selectedAccount) return 0;
    const initial = this.selectedAccount.initial_balance || 0;
    if (this.selectedAccount.nature === "debit") {
      return initial + this.totalDebit - this.totalCredit;
    } else {
      return initial + this.totalCredit - this.totalDebit;
    }
  }

  ngOnInit(): void {
    this.loadAccounts();
    this.loadPeriods();
  }

  loadAccounts(): void {
    this.accountingService.getChartOfAccounts(true).subscribe({
      next: (accounts) => {
        this.accounts = accounts;
      },
    });
  }

  loadPeriods(): void {
    this.accountingService.getPeriods().subscribe({
      next: (periods) => {
        this.periods = periods;
      },
    });
  }

  loadLedger(): void {
    if (!this.selectedAccountId) {
      this.ledgerEntries = [];
      this.selectedAccount = null;
      return;
    }

    this.loading = true;
    this.selectedAccount =
      this.accounts.find((a) => a.id === this.selectedAccountId) || null;

    this.accountingService
      .getGeneralLedger(
        this.selectedAccountId,
        this.startDate || undefined,
        this.endDate || undefined,
        this.selectedPeriodId || undefined
      )
      .subscribe({
        next: (entries) => {
          this.ledgerEntries = entries;
          this.loading = false;
        },
        error: () => {
          this.notificationService.error("Error al cargar libro mayor");
          this.loading = false;
        },
      });
  }
}
