import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { AccountingService } from '../../../core/services/accounting.service';
import { NotificationService } from '../../../core/services/notification.service';
import { ConfirmService } from '../../../core/services/confirm.service';
import { JournalEntry, JournalEntryCreate, JournalEntryLineCreate, JournalEntryStatus, ChartOfAccounts, AccountingPeriod } from '../../../core/models/accounting.model';
import { TooltipDirective } from '../../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-journal-entries',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Asientos Contables</h2>
          <p class="text-gray-600 mt-1">Gestiona los asientos contables de tu negocio</p>
        </div>
        <button
          (click)="openModal()"
          class="btn-primary flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <span>Nuevo Asiento</span>
        </button>
      </div>

      <!-- Filtros -->
      <div class="card">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Período</label>
            <select [(ngModel)]="selectedPeriodId" (ngModelChange)="loadEntries()" class="input-field">
              <option [value]="null">Todos los períodos</option>
              <option *ngFor="let period of periods" [value]="period.id">
                {{ period.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Estado</label>
            <select [(ngModel)]="selectedStatus" (ngModelChange)="loadEntries()" class="input-field">
              <option value="">Todos los estados</option>
              <option [value]="JournalEntryStatus.DRAFT">Borrador</option>
              <option [value]="JournalEntryStatus.POSTED">Contabilizado</option>
            </select>
          </div>
          <div class="flex items-end">
            <button (click)="loadEntries()" class="btn-secondary w-full">
              🔄 Actualizar
            </button>
          </div>
        </div>
      </div>

      <!-- Lista de Asientos -->
      <div class="card">
        <div *ngIf="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p class="mt-2 text-gray-600">Cargando asientos...</p>
        </div>

        <div *ngIf="!loading && entries.length === 0" class="text-center py-8 text-gray-500">
          No hay asientos registrados
        </div>

        <div *ngIf="!loading && entries.length > 0" class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>Número</th>
                <th>Fecha</th>
                <th>Descripción</th>
                <th>Referencia</th>
                <th>Débito</th>
                <th>Crédito</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let entry of entries">
                <td class="font-mono font-semibold">{{ entry.entry_number }}</td>
                <td>{{ entry.entry_date | date:'short' }}</td>
                <td>
                  <p class="font-medium">{{ entry.description }}</p>
                  <p *ngIf="entry.reference" class="text-xs text-gray-500">{{ entry.reference }}</p>
                </td>
                <td>{{ entry.reference || '-' }}</td>
                <td class="text-right font-semibold text-green-600">
                  {{ entry.total_debit | number:'1.2-2' }}
                </td>
                <td class="text-right font-semibold text-red-600">
                  {{ entry.total_credit | number:'1.2-2' }}
                </td>
                <td>
                  <span [class]="'badge ' + getStatusClass(entry.status)">
                    {{ getStatusLabel(entry.status) }}
                  </span>
                </td>
                <td>
                  <div class="flex gap-2">
                    <button
                      (click)="viewEntry(entry)"
                      class="btn-secondary text-sm py-1 px-3"
                      title="Ver detalles"
                    >
                      👁️
                    </button>
                    <button
                      *ngIf="entry.status === JournalEntryStatus.DRAFT"
                      (click)="openModal(entry)"
                      class="btn-secondary text-sm py-1 px-3"
                      title="Editar"
                    >
                      ✏️
                    </button>
                    <button
                      *ngIf="entry.status === JournalEntryStatus.DRAFT"
                      (click)="postEntry(entry)"
                      class="btn-success text-sm py-1 px-3"
                      title="Contabilizar"
                    >
                      ✅
                    </button>
                    <button
                      *ngIf="entry.status === JournalEntryStatus.DRAFT"
                      (click)="deleteEntry(entry)"
                      class="btn-danger text-sm py-1 px-3"
                      title="Eliminar"
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

    <!-- Modal de Asiento -->
    <div
      *ngIf="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      (click)="closeModal()"
    >
      <div
        class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto"
        (click)="$event.stopPropagation()"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-gray-900">
              {{ editingEntry ? 'Editar Asiento' : 'Nuevo Asiento' }}
            </h3>
            <button (click)="closeModal()" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <form [formGroup]="entryForm" (ngSubmit)="saveEntry()">
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Fecha *
                  </label>
                  <input
                    type="datetime-local"
                    formControlName="entry_date"
                    class="input-field"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Período
                  </label>
                  <select formControlName="period_id" class="input-field">
                    <option [value]="null">Seleccionar período</option>
                    <option *ngFor="let period of periods" [value]="period.id">
                      {{ period.name }}
                    </option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Descripción *
                </label>
                <textarea
                  formControlName="description"
                  rows="2"
                  class="input-field"
                  placeholder="Descripción del asiento"
                ></textarea>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Referencia
                </label>
                <input
                  type="text"
                  formControlName="reference"
                  class="input-field"
                  placeholder="Referencia externa (opcional)"
                />
              </div>

              <!-- Líneas del Asiento -->
              <div>
                <div class="flex items-center justify-between mb-3">
                  <label class="block text-sm font-medium text-gray-700">
                    Líneas del Asiento *
                  </label>
                  <button
                    type="button"
                    (click)="addLine()"
                    class="btn-secondary text-sm"
                  >
                    + Agregar Línea
                  </button>
                </div>

                <div class="space-y-3">
                  <div
                    *ngFor="let line of linesArray.controls; let i = index"
                    class="p-4 border rounded-lg bg-gray-50"
                  >
                    <div class="grid grid-cols-1 md:grid-cols-12 gap-3">
                      <div class="md:col-span-4">
                        <label class="block text-xs font-medium text-gray-700 mb-1">
                          Cuenta *
                        </label>
                        <select
                          [formControl]="getLineControl(i, 'account_id')"
                          class="input-field text-sm"
                        >
                          <option value="">Seleccionar cuenta</option>
                          <option *ngFor="let account of accounts" [value]="account.id">
                            {{ account.code }} - {{ account.name }}
                          </option>
                        </select>
                      </div>

                      <div class="md:col-span-3">
                        <label class="block text-xs font-medium text-gray-700 mb-1">
                          Débito
                        </label>
                        <input
                          type="number"
                          [formControl]="getLineControl(i, 'debit')"
                          step="0.01"
                          min="0"
                          class="input-field text-sm"
                          placeholder="0.00"
                          (input)="calculateTotals()"
                        />
                      </div>

                      <div class="md:col-span-3">
                        <label class="block text-xs font-medium text-gray-700 mb-1">
                          Crédito
                        </label>
                        <input
                          type="number"
                          [formControl]="getLineControl(i, 'credit')"
                          step="0.01"
                          min="0"
                          class="input-field text-sm"
                          placeholder="0.00"
                          (input)="calculateTotals()"
                        />
                      </div>

                      <div class="md:col-span-2 flex items-end">
                        <button
                          type="button"
                          (click)="removeLine(i)"
                          class="btn-danger text-sm w-full"
                          [disabled]="linesArray.length === 1"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>

                    <div class="mt-2">
                      <input
                        type="text"
                        [formControl]="getLineControl(i, 'description')"
                        class="input-field text-sm"
                        placeholder="Descripción de la línea (opcional)"
                      />
                    </div>
                  </div>
                </div>

                <!-- Totales -->
                <div class="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <span class="text-sm font-medium text-gray-700">Total Débito:</span>
                      <p class="text-lg font-bold" [class.text-green-600]="totalDebit === totalCredit" [class.text-red-600]="totalDebit !== totalCredit">
                        {{ totalDebit | number:'1.2-2' }}
                      </p>
                    </div>
                    <div>
                      <span class="text-sm font-medium text-gray-700">Total Crédito:</span>
                      <p class="text-lg font-bold" [class.text-green-600]="totalDebit === totalCredit" [class.text-red-600]="totalDebit !== totalCredit">
                        {{ totalCredit | number:'1.2-2' }}
                      </p>
                    </div>
                  </div>
                  <div *ngIf="totalDebit !== totalCredit" class="mt-2 text-sm text-red-600">
                    ⚠️ El asiento no está balanceado. Diferencia: {{ (totalDebit - totalCredit) | number:'1.2-2' }}
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-6 flex justify-end space-x-3">
              <button type="button" (click)="closeModal()" class="btn-secondary">
                Cancelar
              </button>
              <button
                type="submit"
                [disabled]="entryForm.invalid || totalDebit !== totalCredit || linesArray.length === 0"
                class="btn-primary"
              >
                {{ editingEntry ? 'Actualizar' : 'Crear' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Detalle -->
    <div
      *ngIf="showDetailModal && selectedEntry"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      (click)="closeDetailModal()"
    >
      <div
        class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
        (click)="$event.stopPropagation()"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-gray-900">
              Asiento #{{ selectedEntry.entry_number }}
            </h3>
            <button (click)="closeDetailModal()" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <span class="text-sm text-gray-600">Fecha:</span>
                <p class="font-medium">{{ selectedEntry.entry_date | date:'short' }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-600">Estado:</span>
                <p>
                  <span [class]="'badge ' + getStatusClass(selectedEntry.status)">
                    {{ getStatusLabel(selectedEntry.status) }}
                  </span>
                </p>
              </div>
              <div class="col-span-2">
                <span class="text-sm text-gray-600">Descripción:</span>
                <p class="font-medium">{{ selectedEntry.description }}</p>
              </div>
              <div *ngIf="selectedEntry.reference" class="col-span-2">
                <span class="text-sm text-gray-600">Referencia:</span>
                <p class="font-medium">{{ selectedEntry.reference }}</p>
              </div>
            </div>

            <div class="mt-6">
              <h4 class="font-bold mb-3">Líneas del Asiento</h4>
              <div class="table-container">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Cuenta</th>
                      <th>Descripción</th>
                      <th class="text-right">Débito</th>
                      <th class="text-right">Crédito</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr *ngFor="let line of selectedEntry.lines">
                      <td class="font-mono">{{ line.account_code || 'N/A' }}</td>
                      <td>{{ line.description || '-' }}</td>
                      <td class="text-right text-green-600">{{ line.debit | number:'1.2-2' }}</td>
                      <td class="text-right text-red-600">{{ line.credit | number:'1.2-2' }}</td>
                    </tr>
                    <tr class="font-bold bg-gray-100">
                      <td colspan="2" class="text-right">TOTALES:</td>
                      <td class="text-right text-green-600">{{ selectedEntry.total_debit | number:'1.2-2' }}</td>
                      <td class="text-right text-red-600">{{ selectedEntry.total_credit | number:'1.2-2' }}</td>
                    </tr>
                  </tbody>
                </table>
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
export class JournalEntriesComponent implements OnInit {
  private accountingService = inject(AccountingService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);

  entries: JournalEntry[] = [];
  accounts: ChartOfAccounts[] = [];
  periods: AccountingPeriod[] = [];
  loading = true;
  showModal = false;
  showDetailModal = false;
  editingEntry: JournalEntry | null = null;
  selectedEntry: JournalEntry | null = null;
  selectedPeriodId: number | null = null;
  selectedStatus: string = '';

  JournalEntryStatus = JournalEntryStatus;

  entryForm!: FormGroup;
  totalDebit = 0;
  totalCredit = 0;

  ngOnInit(): void {
    this.initForm();
    this.loadAccounts();
    this.loadPeriods();
    this.loadEntries();
  }

  initForm(): void {
    this.entryForm = this.fb.group({
      entry_date: [new Date().toISOString().slice(0, 16), Validators.required],
      reference: [''],
      description: ['', Validators.required],
      period_id: [null],
      lines: this.fb.array([])
    });
    this.addLine();
  }

  get linesArray(): FormArray {
    return this.entryForm.get('lines') as FormArray;
  }

  getLineControl(index: number, field: string) {
    return this.linesArray.at(index).get(field)!;
  }

  addLine(): void {
    const line = this.fb.group({
      account_id: ['', Validators.required],
      debit: [0, [Validators.required, Validators.min(0)]],
      credit: [0, [Validators.required, Validators.min(0)]],
      description: ['']
    });
    this.linesArray.push(line);
    this.calculateTotals();
  }

  removeLine(index: number): void {
    if (this.linesArray.length > 1) {
      this.linesArray.removeAt(index);
      this.calculateTotals();
    }
  }

  calculateTotals(): void {
    this.totalDebit = this.linesArray.controls.reduce((sum, control) => {
      return sum + (Number(control.get('debit')?.value) || 0);
    }, 0);
    
    this.totalCredit = this.linesArray.controls.reduce((sum, control) => {
      return sum + (Number(control.get('credit')?.value) || 0);
    }, 0);
  }

  loadAccounts(): void {
    this.accountingService.getChartOfAccounts(true).subscribe({
      next: (accounts) => {
        this.accounts = accounts;
      }
    });
  }

  loadPeriods(): void {
    this.accountingService.getPeriods().subscribe({
      next: (periods) => {
        this.periods = periods;
      }
    });
  }

  loadEntries(): void {
    this.loading = true;
    this.accountingService.getJournalEntries(0, 100, this.selectedPeriodId || undefined, this.selectedStatus || undefined).subscribe({
      next: (entries) => {
        this.entries = entries;
        this.loading = false;
      },
      error: () => {
        this.notificationService.error('Error al cargar asientos');
        this.loading = false;
      }
    });
  }

  openModal(entry?: JournalEntry): void {
    this.editingEntry = entry || null;
    if (entry) {
      const entryDate = new Date(entry.entry_date);
      const localDateTime = new Date(entryDate.getTime() - entryDate.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
      
      this.entryForm.patchValue({
        entry_date: localDateTime,
        reference: entry.reference || '',
        description: entry.description,
        period_id: entry.period_id || null
      });

      this.linesArray.clear();
      entry.lines.forEach(line => {
        this.linesArray.push(this.fb.group({
          account_id: [line.account_id, Validators.required],
          debit: [line.debit, [Validators.required, Validators.min(0)]],
          credit: [line.credit, [Validators.required, Validators.min(0)]],
          description: [line.description || '']
        }));
      });
    } else {
      this.entryForm.reset({
        entry_date: new Date().toISOString().slice(0, 16),
        reference: '',
        description: '',
        period_id: null
      });
      this.linesArray.clear();
      this.addLine();
    }
    this.calculateTotals();
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.editingEntry = null;
    this.entryForm.reset();
    this.linesArray.clear();
    this.addLine();
  }

  saveEntry(): void {
    if (this.entryForm.invalid || this.totalDebit !== this.totalCredit) return;

    const formValue = this.entryForm.value;
    const entryData: JournalEntryCreate = {
      entry_date: new Date(formValue.entry_date).toISOString(),
      reference: formValue.reference || undefined,
      description: formValue.description,
      period_id: formValue.period_id || undefined,
      lines: formValue.lines.map((line: any) => ({
        account_id: Number(line.account_id),
        debit: Number(line.debit) || 0,
        credit: Number(line.credit) || 0,
        description: line.description || undefined
      }))
    };

    if (this.editingEntry) {
      this.accountingService.updateJournalEntry(this.editingEntry.id, entryData).subscribe({
        next: () => {
          this.notificationService.success('Asiento actualizado exitosamente');
          this.loadEntries();
          this.closeModal();
        },
        error: (err) => {
          this.notificationService.error(err.error?.detail || 'Error al actualizar asiento');
        }
      });
    } else {
      this.accountingService.createJournalEntry(entryData).subscribe({
        next: () => {
          this.notificationService.success('Asiento creado exitosamente');
          this.loadEntries();
          this.closeModal();
        },
        error: (err) => {
          this.notificationService.error(err.error?.detail || 'Error al crear asiento');
        }
      });
    }
  }

  viewEntry(entry: JournalEntry): void {
    this.selectedEntry = entry;
    this.showDetailModal = true;
  }

  closeDetailModal(): void {
    this.showDetailModal = false;
    this.selectedEntry = null;
  }

  postEntry(entry: JournalEntry): void {
    this.confirmService.confirm({
      title: 'Contabilizar Asiento',
      message: `¿Estás seguro de contabilizar el asiento ${entry.entry_number}? Una vez contabilizado no podrá ser modificado.`,
      confirmText: 'Sí, contabilizar',
      cancelText: 'Cancelar',
      type: 'warning'
    }).subscribe(confirmed => {
      if (confirmed) {
        this.accountingService.postJournalEntry(entry.id).subscribe({
          next: () => {
            this.notificationService.success('Asiento contabilizado exitosamente');
            this.loadEntries();
          },
          error: (err) => {
            this.notificationService.error(err.error?.detail || 'Error al contabilizar asiento');
          }
        });
      }
    });
  }

  deleteEntry(entry: JournalEntry): void {
    this.confirmService.confirmDelete(`asiento ${entry.entry_number}`).subscribe(confirmed => {
      if (confirmed) {
        this.accountingService.deleteJournalEntry(entry.id).subscribe({
          next: () => {
            this.notificationService.success('Asiento eliminado exitosamente');
            this.loadEntries();
          },
          error: (err) => {
            this.notificationService.error(err.error?.detail || 'Error al eliminar asiento');
          }
        });
      }
    });
  }

  getStatusLabel(status: JournalEntryStatus): string {
    const labels: Record<JournalEntryStatus, string> = {
      [JournalEntryStatus.DRAFT]: 'Borrador',
      [JournalEntryStatus.POSTED]: 'Contabilizado',
      [JournalEntryStatus.REVERSED]: 'Revertido'
    };
    return labels[status] || status;
  }

  getStatusClass(status: JournalEntryStatus): string {
    const classes: Record<JournalEntryStatus, string> = {
      [JournalEntryStatus.DRAFT]: 'badge-warning',
      [JournalEntryStatus.POSTED]: 'badge-success',
      [JournalEntryStatus.REVERSED]: 'badge-secondary'
    };
    return classes[status] || 'badge-secondary';
  }
}

