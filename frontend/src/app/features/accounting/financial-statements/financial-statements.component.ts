import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AccountingService } from '../../../core/services/accounting.service';
import { NotificationService } from '../../../core/services/notification.service';
import { BalanceSheet, IncomeStatement } from '../../../core/models/accounting.model';

@Component({
  selector: 'app-financial-statements',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Estados Financieros</h2>
        <p class="text-gray-600 mt-1">Balance General y Estado de Resultados</p>
      </div>

      <!-- Tabs -->
      <div class="border-b border-gray-200">
        <nav class="flex space-x-8">
          <button
            (click)="activeTab = 'balance'"
            [class]="activeTab === 'balance' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
            class="border-b-2 py-4 px-1 text-sm font-medium whitespace-nowrap"
          >
            Balance General
          </button>
          <button
            (click)="activeTab = 'income'"
            [class]="activeTab === 'income' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
            class="border-b-2 py-4 px-1 text-sm font-medium whitespace-nowrap"
          >
            Estado de Resultados
          </button>
        </nav>
      </div>

      <!-- Balance General -->
      <div *ngIf="activeTab === 'balance'" class="space-y-6">
        <div class="card">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Fecha de Corte *
            </label>
            <input
              type="date"
              [(ngModel)]="balanceSheetDate"
              (ngModelChange)="loadBalanceSheet()"
              class="input-field"
            />
          </div>
        </div>

        <div class="card" *ngIf="balanceSheet">
          <div *ngIf="loadingBalance" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p class="mt-2 text-gray-600">Generando balance general...</p>
          </div>

          <div *ngIf="!loadingBalance">
            <div class="mb-6 text-center">
              <h3 class="text-xl font-bold mb-2">Balance General</h3>
              <p class="text-gray-600">Al {{ balanceSheet.date | date:'longDate' }}</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Activos -->
              <div>
                <h4 class="text-lg font-bold mb-4 text-blue-600">ACTIVOS</h4>
                <div class="space-y-2">
                  <div
                    *ngFor="let asset of balanceSheet.assets"
                    class="flex justify-between py-2 border-b"
                    [style.padding-left.px]="asset.level * 20"
                  >
                    <span>{{ asset.account_name }}</span>
                    <span class="font-semibold">{{ asset.amount | number:'1.2-2' }}</span>
                  </div>
                  <div class="flex justify-between py-3 border-t-2 border-blue-600 font-bold text-lg">
                    <span>TOTAL ACTIVOS</span>
                    <span class="text-blue-600">{{ balanceSheet.total_assets | number:'1.2-2' }}</span>
                  </div>
                </div>
              </div>

              <!-- Pasivos y Patrimonio -->
              <div>
                <h4 class="text-lg font-bold mb-4 text-orange-600">PASIVOS</h4>
                <div class="space-y-2 mb-6">
                  <div
                    *ngFor="let liability of balanceSheet.liabilities"
                    class="flex justify-between py-2 border-b"
                    [style.padding-left.px]="liability.level * 20"
                  >
                    <span>{{ liability.account_name }}</span>
                    <span class="font-semibold">{{ liability.amount | number:'1.2-2' }}</span>
                  </div>
                  <div class="flex justify-between py-3 border-t-2 border-orange-600 font-bold text-lg">
                    <span>TOTAL PASIVOS</span>
                    <span class="text-orange-600">{{ balanceSheet.total_liabilities | number:'1.2-2' }}</span>
                  </div>
                </div>

                <h4 class="text-lg font-bold mb-4 text-green-600">PATRIMONIO</h4>
                <div class="space-y-2">
                  <div
                    *ngFor="let equity of balanceSheet.equity"
                    class="flex justify-between py-2 border-b"
                    [style.padding-left.px]="equity.level * 20"
                  >
                    <span>{{ equity.account_name }}</span>
                    <span class="font-semibold">{{ equity.amount | number:'1.2-2' }}</span>
                  </div>
                  <div class="flex justify-between py-3 border-t-2 border-green-600 font-bold text-lg">
                    <span>TOTAL PATRIMONIO</span>
                    <span class="text-green-600">{{ balanceSheet.total_equity | number:'1.2-2' }}</span>
                  </div>
                </div>

                <div class="mt-6 pt-4 border-t-2 border-gray-400">
                  <div class="flex justify-between font-bold text-xl">
                    <span>TOTAL PASIVOS + PATRIMONIO</span>
                    <span>{{ (balanceSheet.total_liabilities + balanceSheet.total_equity) | number:'1.2-2' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado de Resultados -->
      <div *ngIf="activeTab === 'income'" class="space-y-6">
        <div class="card">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Fecha Inicio *
              </label>
              <input
                type="date"
                [(ngModel)]="incomeStartDate"
                (ngModelChange)="loadIncomeStatement()"
                class="input-field"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Fecha Fin *
              </label>
              <input
                type="date"
                [(ngModel)]="incomeEndDate"
                (ngModelChange)="loadIncomeStatement()"
                class="input-field"
              />
            </div>
          </div>
        </div>

        <div class="card" *ngIf="incomeStatement">
          <div *ngIf="loadingIncome" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p class="mt-2 text-gray-600">Generando estado de resultados...</p>
          </div>

          <div *ngIf="!loadingIncome">
            <div class="mb-6 text-center">
              <h3 class="text-xl font-bold mb-2">Estado de Resultados</h3>
              <p class="text-gray-600">
                Del {{ incomeStatement.period_start | date:'shortDate' }} al {{ incomeStatement.period_end | date:'shortDate' }}
              </p>
            </div>

            <div class="max-w-2xl mx-auto">
              <!-- Ingresos -->
              <div class="mb-6">
                <h4 class="text-lg font-bold mb-4 text-green-600">INGRESOS</h4>
                <div class="space-y-2">
                  <div
                    *ngFor="let revenue of incomeStatement.revenue"
                    class="flex justify-between py-2 border-b"
                    [style.padding-left.px]="revenue.level * 20"
                  >
                    <span>{{ revenue.account_name }}</span>
                    <span class="font-semibold text-green-600">{{ revenue.amount | number:'1.2-2' }}</span>
                  </div>
                  <div class="flex justify-between py-3 border-t-2 border-green-600 font-bold text-lg">
                    <span>TOTAL INGRESOS</span>
                    <span class="text-green-600">{{ incomeStatement.total_revenue | number:'1.2-2' }}</span>
                  </div>
                </div>
              </div>

              <!-- Costo de Ventas -->
              <div class="mb-6">
                <h4 class="text-lg font-bold mb-4 text-red-600">COSTO DE VENTAS</h4>
                <div class="space-y-2">
                  <div
                    *ngFor="let cost of incomeStatement.cost_of_sales"
                    class="flex justify-between py-2 border-b"
                    [style.padding-left.px]="cost.level * 20"
                  >
                    <span>{{ cost.account_name }}</span>
                    <span class="font-semibold text-red-600">{{ cost.amount | number:'1.2-2' }}</span>
                  </div>
                  <div class="flex justify-between py-3 border-t-2 border-red-600 font-bold text-lg">
                    <span>TOTAL COSTO DE VENTAS</span>
                    <span class="text-red-600">{{ incomeStatement.total_cost_of_sales | number:'1.2-2' }}</span>
                  </div>
                </div>
              </div>

              <!-- Utilidad Bruta -->
              <div class="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div class="flex justify-between font-bold text-xl">
                  <span>UTILIDAD BRUTA</span>
                  <span [class.text-green-600]="incomeStatement.gross_profit >= 0" [class.text-red-600]="incomeStatement.gross_profit < 0">
                    {{ incomeStatement.gross_profit | number:'1.2-2' }}
                  </span>
                </div>
              </div>

              <!-- Gastos -->
              <div class="mb-6">
                <h4 class="text-lg font-bold mb-4 text-orange-600">GASTOS</h4>
                <div class="space-y-2">
                  <div
                    *ngFor="let expense of incomeStatement.expenses"
                    class="flex justify-between py-2 border-b"
                    [style.padding-left.px]="expense.level * 20"
                  >
                    <span>{{ expense.account_name }}</span>
                    <span class="font-semibold text-orange-600">{{ expense.amount | number:'1.2-2' }}</span>
                  </div>
                  <div class="flex justify-between py-3 border-t-2 border-orange-600 font-bold text-lg">
                    <span>TOTAL GASTOS</span>
                    <span class="text-orange-600">{{ incomeStatement.total_expenses | number:'1.2-2' }}</span>
                  </div>
                </div>
              </div>

              <!-- Utilidad Neta -->
              <div class="mt-6 p-4 bg-gray-100 rounded-lg border-2 border-gray-400">
                <div class="flex justify-between font-bold text-2xl">
                  <span>UTILIDAD NETA</span>
                  <span [class.text-green-600]="incomeStatement.net_income >= 0" [class.text-red-600]="incomeStatement.net_income < 0">
                    {{ incomeStatement.net_income | number:'1.2-2' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
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
export class FinancialStatementsComponent implements OnInit {
  private accountingService = inject(AccountingService);
  private notificationService = inject(NotificationService);

  activeTab: 'balance' | 'income' = 'balance';
  balanceSheet: BalanceSheet | null = null;
  incomeStatement: IncomeStatement | null = null;
  balanceSheetDate: string = new Date().toISOString().split('T')[0];
  incomeStartDate: string = new Date(new Date().getFullYear(), 0, 1).toISOString().split('T')[0];
  incomeEndDate: string = new Date().toISOString().split('T')[0];
  loadingBalance = false;
  loadingIncome = false;

  ngOnInit(): void {
    this.loadBalanceSheet();
    this.loadIncomeStatement();
  }

  loadBalanceSheet(): void {
    if (!this.balanceSheetDate) return;

    this.loadingBalance = true;
    this.accountingService.getBalanceSheet(this.balanceSheetDate).subscribe({
      next: (data) => {
        this.balanceSheet = data;
        this.loadingBalance = false;
      },
      error: () => {
        this.notificationService.error('Error al generar balance general');
        this.loadingBalance = false;
      }
    });
  }

  loadIncomeStatement(): void {
    if (!this.incomeStartDate || !this.incomeEndDate) return;

    this.loadingIncome = true;
    this.accountingService.getIncomeStatement(this.incomeStartDate, this.incomeEndDate).subscribe({
      next: (data) => {
        this.incomeStatement = data;
        this.loadingIncome = false;
      },
      error: () => {
        this.notificationService.error('Error al generar estado de resultados');
        this.loadingIncome = false;
      }
    });
  }
}

