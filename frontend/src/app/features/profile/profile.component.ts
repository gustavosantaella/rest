import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { ProfileService } from '../../core/services/profile.service';
import { AuthService } from '../../core/services/auth.service';
import { NotificationService } from '../../core/services/notification.service';
import { TutorialService } from '../../core/services/tutorial.service';
import { User, UserRole } from '../../core/models/user.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, TooltipDirective],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  private profileService = inject(ProfileService);
  private authService = inject(AuthService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);
  private tutorialService = inject(TutorialService);
  
  currentUser: User | null = null;
  profileForm!: FormGroup;
  passwordForm!: FormGroup;
  
  savingProfile = false;
  savingPassword = false;
  
  // Modal de eliminación de cuenta
  showDeleteModal = false;
  deletePassword = '';
  deletingAccount = false;
  deleteConfirmationText = '';
  REQUIRED_DELETE_TEXT = 'ELIMINAR TODO';
  
  countries = [
    'Venezuela', 'Colombia', 'México', 'Argentina', 'Chile', 'Perú',
    'Ecuador', 'Bolivia', 'Uruguay', 'Paraguay', 'España', 'Estados Unidos'
  ];
  
  constructor() {
    this.initForms();
  }
  
  ngOnInit(): void {
    this.loadProfile();
  }
  
  initForms(): void {
    this.profileForm = this.fb.group({
      full_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      dni: [''],
      country: ['']
    });
    
    this.passwordForm = this.fb.group({
      current_password: ['', Validators.required],
      new_password: ['', [Validators.required, Validators.minLength(6)]],
      confirm_password: ['', Validators.required]
    }, { validators: this.passwordMatchValidator });
  }
  
  passwordMatchValidator(form: FormGroup) {
    const newPassword = form.get('new_password');
    const confirmPassword = form.get('confirm_password');
    
    if (newPassword && confirmPassword && newPassword.value !== confirmPassword.value) {
      confirmPassword.setErrors({ mismatch: true });
      return { mismatch: true };
    }
    return null;
  }
  
  loadProfile(): void {
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.currentUser = user;
        this.profileForm.patchValue({
          full_name: user.full_name,
          email: user.email,
          dni: user.dni || '',
          country: user.country || ''
        });
      }
    });
  }
  
  saveProfile(): void {
    if (this.profileForm.invalid) return;
    
    this.savingProfile = true;
    
    this.profileService.updateMyProfile(this.profileForm.value).subscribe({
      next: (user) => {
        this.savingProfile = false;
        this.notificationService.success('Perfil actualizado exitosamente');
        // Recargar el usuario actual
        this.authService.setToken(this.authService.getToken()!);
        window.location.reload();
      },
      error: (err) => {
        this.savingProfile = false;
        this.notificationService.error('Error al actualizar perfil: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
  
  changePassword(): void {
    if (this.passwordForm.invalid) return;
    
    this.savingPassword = true;
    
    const { current_password, new_password } = this.passwordForm.value;
    
    this.profileService.changePassword({ current_password, new_password }).subscribe({
      next: (response) => {
        this.savingPassword = false;
        this.passwordForm.reset();
        this.notificationService.success('Contraseña cambiada exitosamente. Por seguridad, debes iniciar sesión nuevamente.');
        setTimeout(() => {
          this.authService.logout();
        }, 2000);
      },
      error: (err) => {
        this.savingPassword = false;
        this.notificationService.error('Error: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
  
  // Métodos para eliminación de cuenta
  isAdmin(): boolean {
    return this.currentUser?.role === UserRole.ADMIN;
  }
  
  openDeleteModal(): void {
    this.showDeleteModal = true;
    this.deletePassword = '';
    this.deleteConfirmationText = '';
  }
  
  closeDeleteModal(): void {
    this.showDeleteModal = false;
    this.deletePassword = '';
    this.deleteConfirmationText = '';
  }
  
  canConfirmDelete(): boolean {
    return this.deletePassword.trim() !== '' && 
           this.deleteConfirmationText === this.REQUIRED_DELETE_TEXT;
  }
  
  deleteAccountPermanently(): void {
    if (!this.canConfirmDelete()) {
      return;
    }
    
    this.deletingAccount = true;
    
    this.profileService.deleteAccountPermanently(this.deletePassword).subscribe({
      next: (response) => {
        this.deletingAccount = false;
        this.notificationService.success(response.message);
        this.notificationService.warning(response.warning);
        
        // Cerrar sesión después de 3 segundos
        setTimeout(() => {
          this.authService.logout();
        }, 3000);
      },
      error: (err) => {
        this.deletingAccount = false;
        this.notificationService.error('Error: ' + (err.error?.detail || 'Error al eliminar la cuenta'));
      }
    });
  }
  
  restartTutorial(): void {
    this.tutorialService.resetTutorial();
    this.tutorialService.startTutorial();
    this.notificationService.success('Tutorial iniciado. Te guiaremos paso a paso.');
  }
}

