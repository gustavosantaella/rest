import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AccountingService } from '../../../core/services/accounting.service';
import { NotificationService } from '../../../core/services/notification.service';
import { ConfirmService } from '../../../core/services/confirm.service';
import { AccountingPeriod, AccountingPeriodCreate } from '../../../core/models/accounting.model';
import { TooltipDirective } from '../../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-periods',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, TooltipDirective],
  template: `
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Períodos Contables</h2>
          <p class="text-gray-600 mt-1">Gestiona los períodos contables de tu negocio</p>
        </div>
        <button
          (click)="openModal()"
          class="btn-primary flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <span>Nuevo Período</span>
        </button>
      </div>

      <!-- Lista de Períodos -->
      <div class="card">
        <div *ngIf="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p class="mt-2 text-gray-600">Cargando períodos...</p>
        </div>

        <div *ngIf="!loading && periods.length === 0" class="text-center py-8 text-gray-500">
          No hay períodos contables registrados
        </div>

        <div *ngIf="!loading && periods.length > 0" class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Fecha Inicio</th>
                <th>Fecha Fin</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let period of periods" [class.bg-gray-50]="period.is_closed">
                <td class="font-semibold">{{ period.name }}</td>
                <td>{{ period.start_date | date:'shortDate' }}</td>
                <td>{{ period.end_date | date:'shortDate' }}</td>
                <td>
                  <span [class]="'badge ' + (period.is_closed ? 'badge-success' : 'badge-warning')">
                    {{ period.is_closed ? 'Cerrado' : 'Abierto' }}
                  </span>
                </td>
                <td>
                  <div class="flex gap-2">
                    <button
                      *ngIf="!period.is_closed"
                      (click)="closePeriod(period)"
                      class="btn-success text-sm py-1 px-3"
                      title="Cerrar período"
                    >
                      🔒 Cerrar
                    </button>
                    <button
                      (click)="openModal(period)"
                      class="btn-secondary text-sm py-1 px-3"
                      [disabled]="period.is_closed"
                      title="Editar período"
                    >
                      ✏️
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Período -->
    <div
      *ngIf="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      (click)="closeModal()"
    >
      <div
        class="bg-white rounded-lg shadow-xl max-w-2xl w-full"
        (click)="$event.stopPropagation()"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-gray-900">
              {{ editingPeriod ? 'Editar Período' : 'Nuevo Período' }}
            </h3>
            <button (click)="closeModal()" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <form [formGroup]="periodForm" (ngSubmit)="savePeriod()">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre *
                </label>
                <input
                  type="text"
                  formControlName="name"
                  class="input-field"
                  placeholder="Ej: Enero 2024"
                  appTooltip="Nombre descriptivo del período contable"
                  tooltipPosition="top"
                />
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Fecha Inicio *
                  </label>
                  <input
                    type="date"
                    formControlName="start_date"
                    class="input-field"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Fecha Fin *
                  </label>
                  <input
                    type="date"
                    formControlName="end_date"
                    class="input-field"
                  />
                </div>
              </div>
            </div>

            <div class="mt-6 flex justify-end space-x-3">
              <button type="button" (click)="closeModal()" class="btn-secondary">
                Cancelar
              </button>
              <button type="submit" [disabled]="periodForm.invalid" class="btn-primary">
                {{ editingPeriod ? 'Actualizar' : 'Crear' }}
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
export class PeriodsComponent implements OnInit {
  private accountingService = inject(AccountingService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);

  periods: AccountingPeriod[] = [];
  loading = true;
  showModal = false;
  editingPeriod: AccountingPeriod | null = null;

  periodForm!: FormGroup;

  ngOnInit(): void {
    this.initForm();
    this.loadPeriods();
  }

  initForm(): void {
    this.periodForm = this.fb.group({
      name: ['', Validators.required],
      start_date: ['', Validators.required],
      end_date: ['', Validators.required]
    });
  }

  loadPeriods(): void {
    this.loading = true;
    this.accountingService.getPeriods().subscribe({
      next: (periods) => {
        this.periods = periods;
        this.loading = false;
      },
      error: () => {
        this.notificationService.error('Error al cargar períodos');
        this.loading = false;
      }
    });
  }

  openModal(period?: AccountingPeriod): void {
    this.editingPeriod = period || null;
    if (period) {
      this.periodForm.patchValue({
        name: period.name,
        start_date: period.start_date.split('T')[0],
        end_date: period.end_date.split('T')[0]
      });
    } else {
      this.periodForm.reset();
    }
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.editingPeriod = null;
    this.periodForm.reset();
  }

  savePeriod(): void {
    if (this.periodForm.invalid) return;

    const periodData: AccountingPeriodCreate = {
      name: this.periodForm.value.name,
      start_date: new Date(this.periodForm.value.start_date).toISOString(),
      end_date: new Date(this.periodForm.value.end_date).toISOString()
    };

    if (this.editingPeriod) {
      this.accountingService.updatePeriod(this.editingPeriod.id, periodData).subscribe({
        next: () => {
          this.notificationService.success('Período actualizado exitosamente');
          this.loadPeriods();
          this.closeModal();
        },
        error: (err) => {
          this.notificationService.error(err.error?.detail || 'Error al actualizar período');
        }
      });
    } else {
      this.accountingService.createPeriod(periodData).subscribe({
        next: () => {
          this.notificationService.success('Período creado exitosamente');
          this.loadPeriods();
          this.closeModal();
        },
        error: (err) => {
          this.notificationService.error(err.error?.detail || 'Error al crear período');
        }
      });
    }
  }

  closePeriod(period: AccountingPeriod): void {
    this.confirmService.confirm({
      title: 'Cerrar Período',
      message: `¿Estás seguro de cerrar el período "${period.name}"? Una vez cerrado no podrá ser modificado.`,
      confirmText: 'Sí, cerrar',
      cancelText: 'Cancelar',
      type: 'warning'
    }).subscribe(confirmed => {
      if (confirmed) {
        this.accountingService.closePeriod(period.id).subscribe({
          next: () => {
            this.notificationService.success('Período cerrado exitosamente');
            this.loadPeriods();
          },
          error: (err) => {
            this.notificationService.error(err.error?.detail || 'Error al cerrar período');
          }
        });
      }
    });
  }
}

