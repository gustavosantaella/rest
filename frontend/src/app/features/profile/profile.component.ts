import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ProfileService } from '../../core/services/profile.service';
import { AuthService } from '../../core/services/auth.service';
import { User } from '../../core/models/user.model';
import { TooltipDirective } from '../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, TooltipDirective],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  private profileService = inject(ProfileService);
  private authService = inject(AuthService);
  private fb = inject(FormBuilder);
  
  currentUser: User | null = null;
  profileForm!: FormGroup;
  passwordForm!: FormGroup;
  
  savingProfile = false;
  savingPassword = false;
  
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
        alert('Perfil actualizado exitosamente');
        // Recargar el usuario actual
        this.authService.setToken(this.authService.getToken()!);
        window.location.reload();
      },
      error: (err) => {
        this.savingProfile = false;
        alert('Error al actualizar perfil: ' + (err.error?.detail || 'Error desconocido'));
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
        alert('Contraseña cambiada exitosamente. Por seguridad, debes iniciar sesión nuevamente.');
        this.authService.logout();
      },
      error: (err) => {
        this.savingPassword = false;
        alert('Error: ' + (err.error?.detail || 'Error desconocido'));
      }
    });
  }
}

