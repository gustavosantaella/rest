import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { TooltipDirective } from '../../../shared/directives/tooltip.directive';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink, TooltipDirective],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  
  loginForm: FormGroup;
  loading = false;
  error = '';
  successMessage = '';
  returnUrl = '/dashboard';
  
  constructor() {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }
  
  ngOnInit(): void {
    // Si ya está autenticado, redirigir
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }
    
    // Verificar si viene de un registro exitoso
    const queryParams = this.route.snapshot.queryParams;
    if (queryParams['registered'] === 'true' && queryParams['email']) {
      this.successMessage = '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.';
      // Pre-llenar el username con la parte del email
      const username = queryParams['email'].split('@')[0];
      this.loginForm.patchValue({ username });
    }
    
    // Obtener URL de retorno si existe
    this.returnUrl = queryParams['returnUrl'] || '/dashboard';
  }
  
  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }
    
    this.loading = true;
    this.error = '';
    
    this.authService.login(this.loginForm.value).subscribe({
      next: () => {
        // Redirigir a la URL que intentaba acceder o al dashboard
        this.router.navigateByUrl(this.returnUrl);
      },
      error: (err) => {
        this.error = 'Usuario o contraseña incorrectos';
        this.loading = false;
      }
    });
  }
}

