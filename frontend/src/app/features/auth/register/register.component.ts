import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { RegisterRequest } from '../../../core/models/user.model';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  registerForm: FormGroup;
  loading = false;
  errorMessage = '';
  successMessage = '';

  constructor() {
    this.registerForm = this.fb.group({
      // Datos del usuario
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      full_name: ['', Validators.required],
      
      // Datos del negocio
      business_name: ['', Validators.required],
      legal_name: [''],
      phone: ['']
    });
  }

  onSubmit(): void {
    if (this.registerForm.invalid) return;

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const registerData: RegisterRequest = this.registerForm.value;

    this.authService.register(registerData).subscribe({
      next: (response) => {
        this.loading = false;
        this.successMessage = `¡Registro exitoso! Tu catálogo público estará en /catalog/${response.business_slug}`;
        
        // Redirigir al login después de 3 segundos
        setTimeout(() => {
          this.router.navigate(['/login'], {
            queryParams: { registered: 'true', email: response.user_email }
          });
        }, 3000);
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = error.error?.detail || 'Error al registrar. Intenta nuevamente.';
      }
    });
  }
}

