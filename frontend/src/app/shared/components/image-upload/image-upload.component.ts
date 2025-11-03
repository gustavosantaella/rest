import { Component, Input, Output, EventEmitter, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { UploadService } from '../../../core/services/upload.service';

@Component({
  selector: 'app-image-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-3">
      <!-- Opción: URL o Archivo -->
      <div class="flex items-center space-x-4 text-sm">
        <label class="flex items-center cursor-pointer">
          <input 
            type="radio" 
            [checked]="uploadMode === 'url'"
            (change)="uploadMode = 'url'; clearFile()"
            class="mr-2"
          >
          <span>URL de imagen</span>
        </label>
        <label class="flex items-center cursor-pointer">
          <input 
            type="radio" 
            [checked]="uploadMode === 'file'"
            (change)="uploadMode = 'file'; clearUrl()"
            class="mr-2"
          >
          <span>Subir archivo</span>
        </label>
      </div>

      <!-- Input de URL -->
      <div *ngIf="uploadMode === 'url'" class="space-y-2">
        <input
          type="url"
          [(ngModel)]="imageUrl"
          (ngModelChange)="onUrlChange($event)"
          placeholder="https://ejemplo.com/imagen.jpg"
          class="input-field"
        />
        <p class="text-xs text-gray-500">Ingresa la URL completa de la imagen</p>
      </div>

      <!-- Input de Archivo -->
      <div *ngIf="uploadMode === 'file'" class="space-y-2">
        <input
          type="file"
          accept="image/*"
          (change)="onFileSelected($event)"
          #fileInput
          class="input-field"
        />
        <p class="text-xs text-gray-500">Formatos: JPG, PNG, GIF, WEBP (máx. 5MB)</p>
        
        <!-- Mensaje de carga -->
        <div *ngIf="isUploading" class="text-sm text-primary-600 flex items-center">
          <svg class="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Subiendo imagen...
        </div>

        <!-- Mensaje de error -->
        <div *ngIf="uploadError" class="text-sm text-red-600">
          {{ uploadError }}
        </div>
      </div>

      <!-- Preview de la imagen -->
      <div *ngIf="getImageUrl()" class="relative">
        <img 
          [src]="getImageUrl()" 
          alt="Preview"
          class="w-full h-48 object-cover rounded-lg border-2 border-gray-200"
          (error)="onImageError()"
        />
        <button
          type="button"
          (click)="removeImage()"
          class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 transition-colors"
          title="Eliminar imagen"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  `,
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => ImageUploadComponent),
      multi: true
    }
  ]
})
export class ImageUploadComponent implements ControlValueAccessor {
  uploadMode: 'url' | 'file' = 'url';
  imageUrl: string = '';
  isUploading: boolean = false;
  uploadError: string = '';
  
  private onChange: (value: string | null) => void = () => {};
  private onTouched: () => void = () => {};

  constructor(private uploadService: UploadService) {}

  writeValue(value: string | null): void {
    if (value) {
      this.imageUrl = value;
      // Detectar si es URL o archivo subido
      if (value.startsWith('http://') || value.startsWith('https://')) {
        this.uploadMode = 'url';
      } else {
        this.uploadMode = 'file';
      }
    } else {
      this.imageUrl = '';
    }
  }

  registerOnChange(fn: (value: string | null) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  onUrlChange(url: string): void {
    this.onChange(url || null);
    this.onTouched();
  }

  async onFileSelected(event: any): Promise<void> {
    const file: File = event.target.files[0];
    if (!file) return;

    // Validar tamaño
    if (file.size > 5 * 1024 * 1024) {
      this.uploadError = 'El archivo es demasiado grande. Tamaño máximo: 5MB';
      return;
    }

    // Validar tipo
    if (!file.type.startsWith('image/')) {
      this.uploadError = 'El archivo debe ser una imagen';
      return;
    }

    this.uploadError = '';
    this.isUploading = true;

    this.uploadService.uploadImage(file).subscribe({
      next: (response) => {
        this.imageUrl = response.image_url;
        this.onChange(response.image_url);
        this.onTouched();
        this.isUploading = false;
      },
      error: (error) => {
        this.uploadError = error.error?.detail || 'Error al subir la imagen';
        this.isUploading = false;
      }
    });
  }

  getImageUrl(): string {
    if (!this.imageUrl) return '';
    return this.uploadService.getFullImageUrl(this.imageUrl);
  }

  removeImage(): void {
    this.imageUrl = '';
    this.onChange(null);
    this.onTouched();
  }

  clearFile(): void {
    this.imageUrl = '';
    this.onChange(null);
  }

  clearUrl(): void {
    this.imageUrl = '';
    this.onChange(null);
  }

  onImageError(): void {
    console.error('Error al cargar la imagen');
  }
}

