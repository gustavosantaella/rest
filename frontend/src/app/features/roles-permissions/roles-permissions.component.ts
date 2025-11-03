import { Component, OnInit, inject } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  FormsModule,
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  Validators,
} from "@angular/forms";
import { RoleService } from "../../core/services/role.service";
import { NotificationService } from "../../core/services/notification.service";
import { ConfirmService } from "../../core/services/confirm.service";
import {
  Role,
  Permission,
  PermissionsByModule,
  SYSTEM_MODULES,
} from "../../core/models/role.model";

@Component({
  selector: "app-roles-permissions",
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: "./roles-permissions.component.html",
  styleUrls: ["./roles-permissions.component.scss"],
})
export class RolesPermissionsComponent implements OnInit {
  private roleService = inject(RoleService);
  private notificationService = inject(NotificationService);
  private confirmService = inject(ConfirmService);
  private fb = inject(FormBuilder);

  roles: Role[] = [];
  allPermissions: Permission[] = [];
  permissionsByModule: PermissionsByModule = {};
  systemModules = SYSTEM_MODULES;

  showRoleModal = false;
  editingRole: Role | null = null;
  roleForm!: FormGroup;

  selectedPermissions: Set<number> = new Set();
  loading = true;

  constructor() {
    this.initForm();
  }

  ngOnInit() {
    this.loadData();
  }

  initForm() {
    this.roleForm = this.fb.group({
      name: ["", Validators.required],
      description: [""],
      is_active: [true],
    });
  }

  loadData() {
    this.loading = true;

    // Cargar roles y permisos en paralelo
    Promise.all([
      this.roleService.getRoles().toPromise(),
      this.roleService.getPermissionsByModule().toPromise(),
    ])
      .then(([roles, permissions]) => {
        this.roles = roles || [];
        this.permissionsByModule = permissions || {};

        // Crear lista plana de permisos
        this.allPermissions = [];
        Object.values(this.permissionsByModule).forEach((perms) => {
          this.allPermissions.push(...perms);
        });

        this.loading = false;
      })
      .catch((err) => {
        this.notificationService.error("Error al cargar datos");
        this.loading = false;
      });
  }

  openRoleModal(role?: Role) {
    this.editingRole = role || null;

    if (role) {
      this.roleForm.patchValue({
        name: role.name,
        description: role.description,
        is_active: role.is_active,
      });
      this.selectedPermissions = new Set(role.permissions.map((p) => p.id));
    } else {
      this.roleForm.reset({ is_active: true });
      this.selectedPermissions = new Set();
    }

    this.showRoleModal = true;
  }

  closeRoleModal() {
    this.showRoleModal = false;
    this.editingRole = null;
    this.selectedPermissions.clear();
  }

  togglePermission(permissionId: number) {
    if (this.selectedPermissions.has(permissionId)) {
      this.selectedPermissions.delete(permissionId);
    } else {
      this.selectedPermissions.add(permissionId);
    }
  }

  toggleAllModulePermissions(module: string) {
    const modulePerms = this.permissionsByModule[module] || [];
    const allSelected = modulePerms.every((p) =>
      this.selectedPermissions.has(p.id)
    );

    if (allSelected) {
      // Deseleccionar todos
      modulePerms.forEach((p) => this.selectedPermissions.delete(p.id));
    } else {
      // Seleccionar todos
      modulePerms.forEach((p) => this.selectedPermissions.add(p.id));
    }
  }

  isModuleFullySelected(module: string): boolean {
    const modulePerms = this.permissionsByModule[module] || [];
    return (
      modulePerms.length > 0 &&
      modulePerms.every((p) => this.selectedPermissions.has(p.id))
    );
  }

  isModulePartiallySelected(module: string): boolean {
    const modulePerms = this.permissionsByModule[module] || [];
    const selectedCount = modulePerms.filter((p) =>
      this.selectedPermissions.has(p.id)
    ).length;
    return selectedCount > 0 && selectedCount < modulePerms.length;
  }

  saveRole() {
    if (this.roleForm.invalid) return;

    const roleData = {
      ...this.roleForm.value,
      permission_ids: Array.from(this.selectedPermissions),
    };

    if (this.editingRole) {
      this.roleService.updateRole(this.editingRole.id, roleData).subscribe({
        next: () => {
          this.loadData();
          this.closeRoleModal();
          this.notificationService.success("Rol actualizado exitosamente");
        },
        error: (err) => {
          this.notificationService.error(
            "Error al actualizar rol: " +
              (err.error?.detail || "Error desconocido")
          );
        },
      });
    } else {
      this.roleService.createRole(roleData).subscribe({
        next: () => {
          this.loadData();
          this.closeRoleModal();
          this.notificationService.success("Rol creado exitosamente");
        },
        error: (err) => {
          this.notificationService.error(
            "Error al crear rol: " + (err.error?.detail || "Error desconocido")
          );
        },
      });
    }
  }

  deleteRole(role: Role) {
    this.confirmService
      .confirmDelete(`el rol "${role.name}"`)
      .subscribe((confirmed) => {
        if (confirmed) {
          this.roleService.deleteRole(role.id).subscribe({
            next: () => {
              this.loadData();
              this.notificationService.success("Rol eliminado exitosamente");
            },
            error: (err) => {
              this.notificationService.error(
                "Error al eliminar rol: " +
                  (err.error?.detail || "Error desconocido")
              );
            },
          });
        }
      });
  }

  getModuleIcon(moduleCode: string): string {
    const module = this.systemModules.find((m) => m.code === moduleCode);
    return module?.icon || "📄";
  }

  getModuleName(moduleCode: string): string {
    const module = this.systemModules.find((m) => m.code === moduleCode);
    return module?.name || moduleCode;
  }

  getSelectedPermissionsCount(): number {
    return this.selectedPermissions.size;
  }
}
