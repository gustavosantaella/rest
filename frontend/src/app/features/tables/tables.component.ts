import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { TableService } from '../../core/services/table.service';
import { AuthPermissionsService } from '../../core/services/auth-permissions.service';
import { Table, TableStatus, TableCreate } from '../../core/models/table.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-tables',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterLink, TooltipDirective],
  templateUrl: './tables.component.html',
  styleUrls: ['./tables.component.scss']
})
export class TablesComponent implements OnInit, OnDestroy {
  private tableService = inject(TableService);
  private authPermissionsService = inject(AuthPermissionsService);
  private fb = inject(FormBuilder);
  
  tables: Table[] = [];
  showModal = false;
  editingTable: Table | null = null;
  tableForm!: FormGroup;
  loading = true;
  private refreshInterval: any;
  
  tableStatuses = Object.values(TableStatus);
  statusLabels: Record<TableStatus, string> = {
    [TableStatus.AVAILABLE]: 'Disponible',
    [TableStatus.OCCUPIED]: 'Ocupada',
    [TableStatus.RESERVED]: 'Reservada',
    [TableStatus.CLEANING]: 'Limpieza'
  };
  
  constructor() {
    this.initForm();
  }
  
  ngOnInit(): void {
    this.loadTables();
    
    // Actualizar cada 10 segundos para reflejar cambios de órdenes
    this.refreshInterval = setInterval(() => {
      if (!this.showModal) { // Solo refrescar si no hay modal abierto
        this.loadTables();
      }
    }, 10000);
  }

  ngOnDestroy(): void {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }
  
  initForm(): void {
    this.tableForm = this.fb.group({
      number: ['', Validators.required],
      capacity: [2, [Validators.required, Validators.min(1)]],
      location: ['']
    });
  }
  
  loadTables(): void {
    const isInitialLoad = this.loading;
    if (isInitialLoad) {
      this.loading = true;
    }
    
    this.tableService.getTables().subscribe({
      next: (tables) => {
        this.tables = tables;
        if (isInitialLoad) {
          this.loading = false;
        }
      },
      error: () => {
        if (isInitialLoad) {
          this.loading = false;
        }
      }
    });
  }
  
  openModal(table?: Table): void {
    this.editingTable = table || null;
    
    if (table) {
      this.tableForm.patchValue(table);
    } else {
      this.tableForm.reset({ capacity: 2 });
    }
    
    this.showModal = true;
  }
  
  closeModal(): void {
    this.showModal = false;
    this.editingTable = null;
  }
  
  saveTable(): void {
    if (this.tableForm.invalid) return;
    
    const tableData: TableCreate = this.tableForm.value;
    
    if (this.editingTable) {
      this.tableService.updateTable(this.editingTable.id, tableData).subscribe({
        next: () => {
          this.loadTables();
          this.closeModal();
        }
      });
    } else {
      this.tableService.createTable(tableData).subscribe({
        next: () => {
          this.loadTables();
          this.closeModal();
        }
      });
    }
  }
  
  updateTableStatus(table: Table, status: TableStatus): void {
    this.tableService.updateTable(table.id, { status }).subscribe({
      next: () => {
        this.loadTables();
      }
    });
  }
  
  deleteTable(table: Table): void {
    if (confirm(`¿Estás seguro de eliminar la mesa "${table.number}"?`)) {
      this.tableService.deleteTable(table.id).subscribe({
        next: () => {
          this.loadTables();
        }
      });
    }
  }
  
  getStatusClass(status: TableStatus): string {
    const classes: Record<TableStatus, string> = {
      [TableStatus.AVAILABLE]: 'bg-green-100 text-green-800 border-green-300',
      [TableStatus.OCCUPIED]: 'bg-red-100 text-red-800 border-red-300',
      [TableStatus.RESERVED]: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      [TableStatus.CLEANING]: 'bg-blue-100 text-blue-800 border-blue-300'
    };
    return classes[status];
  }
  
  getTablesByStatus(status: TableStatus): Table[] {
    return this.tables.filter(t => t.status === status);
  }
  
  // Métodos de verificación de permisos
  canViewTables(): boolean {
    return this.authPermissionsService.hasPermission('tables.view');
  }
  
  canManageTables(): boolean {
    return this.authPermissionsService.hasPermission('tables.manage');
  }
}

