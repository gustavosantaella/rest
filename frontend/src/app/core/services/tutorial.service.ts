import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface TutorialStep {
  id: string;
  title: string;
  description: string;
  element: string; // Selector CSS del elemento a resaltar
  position: 'top' | 'bottom' | 'left' | 'right' | 'center';
  action?: 'click' | 'navigate'; // Acción opcional a realizar
  route?: string; // Ruta a navegar si action es 'navigate'
  highlight?: boolean; // Si debe resaltar el elemento
}

@Injectable({
  providedIn: 'root'
})
export class TutorialService {
  private readonly TUTORIAL_KEY = 'tutorial_completed';
  private readonly TUTORIAL_SKIPPED_KEY = 'tutorial_skipped';
  
  private currentStepIndex = 0;
  private isActiveSubject = new BehaviorSubject<boolean>(false);
  private currentStepSubject = new BehaviorSubject<TutorialStep | null>(null);
  
  public isActive$: Observable<boolean> = this.isActiveSubject.asObservable();
  public currentStep$: Observable<TutorialStep | null> = this.currentStepSubject.asObservable();
  
  // Definir todos los pasos del tutorial
  private steps: TutorialStep[] = [
    {
      id: 'welcome',
      title: '¡Bienvenido a tu Sistema de Gestión! 🎉',
      description: 'Te guiaremos paso a paso para que conozcas todas las funcionalidades. Este tutorial tomará aproximadamente 3 minutos.',
      element: '',
      position: 'center',
      highlight: false
    },
    {
      id: 'dashboard',
      title: 'Dashboard 📊',
      description: 'Aquí verás un resumen general: ventas del día, órdenes pendientes, mesas disponibles y más. Es tu centro de control.',
      element: '[data-tutorial="dashboard"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'inventory',
      title: 'Inventario 📦',
      description: 'Gestiona todos tus productos: agregar, editar, controlar stock, categorías y precios. Todo tu inventario en un solo lugar.',
      element: '[data-tutorial="inventory"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'menu',
      title: 'Menú 🍽️',
      description: 'Crea tu menú personalizado con platillos que pueden incluir múltiples productos. Ideal para combos y promociones.',
      element: '[data-tutorial="menu"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'tables',
      title: 'Mesas 🪑',
      description: 'Administra las mesas de tu restaurante: estados (disponible, ocupada, reservada), capacidad y órdenes asignadas.',
      element: '[data-tutorial="tables"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'orders',
      title: 'Órdenes 📋',
      description: 'Gestiona todas las órdenes: crear nuevas, cambiar estados (pendiente, preparando, completada), procesar pagos y más.',
      element: '[data-tutorial="orders"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'users',
      title: 'Usuarios 👥',
      description: 'Administra tu equipo: crear usuarios, asignar roles (admin, gerente, mesero, cajero, chef) y gestionar permisos.',
      element: '[data-tutorial="users"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'customers',
      title: 'Clientes 👨‍👩‍👧',
      description: 'Registra tus clientes con nombre, contacto y DNI. Útil para cuentas por cobrar y historial de compras.',
      element: '[data-tutorial="customers"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'cash-closing',
      title: 'Cierre de Caja 🧮',
      description: 'Genera reportes diarios: ventas totales, desglose por métodos de pago, productos vendidos y listado de órdenes.',
      element: '[data-tutorial="cash-closing"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'accounts',
      title: 'Cuentas 💰💳',
      description: 'Módulo contable completo: registra cuentas por cobrar (clientes que te deben) y cuentas por pagar (proveedores).',
      element: '[data-tutorial="accounts"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'configuration',
      title: 'Configuración ⚙️',
      description: 'Personaliza tu sistema: datos del negocio, socios, métodos de pago, roles personalizados y permisos.',
      element: '[data-tutorial="configuration"]',
      position: 'right',
      highlight: true
    },
    {
      id: 'complete',
      title: '¡Tutorial Completado! ✅',
      description: 'Ya conoces todos los módulos. Puedes volver a ver este tutorial desde tu perfil. ¡Comienza a usar el sistema!',
      element: '',
      position: 'center',
      highlight: false
    }
  ];
  
  constructor() {}
  
  // Verificar si el usuario ya completó el tutorial
  hasCompletedTutorial(): boolean {
    return localStorage.getItem(this.TUTORIAL_KEY) === 'true';
  }
  
  // Verificar si el usuario saltó el tutorial
  hasSkippedTutorial(): boolean {
    return localStorage.getItem(this.TUTORIAL_SKIPPED_KEY) === 'true';
  }
  
  // Marcar tutorial como completado
  markAsCompleted(): void {
    localStorage.setItem(this.TUTORIAL_KEY, 'true');
    localStorage.removeItem(this.TUTORIAL_SKIPPED_KEY);
  }
  
  // Marcar tutorial como saltado
  markAsSkipped(): void {
    localStorage.setItem(this.TUTORIAL_SKIPPED_KEY, 'true');
  }
  
  // Reiniciar tutorial (para poder verlo de nuevo)
  resetTutorial(): void {
    localStorage.removeItem(this.TUTORIAL_KEY);
    localStorage.removeItem(this.TUTORIAL_SKIPPED_KEY);
    this.currentStepIndex = 0;
  }
  
  // Iniciar tutorial
  startTutorial(): void {
    this.currentStepIndex = 0;
    this.isActiveSubject.next(true);
    this.showCurrentStep();
  }
  
  // Detener tutorial
  stopTutorial(): void {
    this.isActiveSubject.next(false);
    this.currentStepSubject.next(null);
  }
  
  // Siguiente paso
  nextStep(): void {
    if (this.currentStepIndex < this.steps.length - 1) {
      this.currentStepIndex++;
      this.showCurrentStep();
    } else {
      // Tutorial completado
      this.markAsCompleted();
      this.stopTutorial();
    }
  }
  
  // Paso anterior
  previousStep(): void {
    if (this.currentStepIndex > 0) {
      this.currentStepIndex--;
      this.showCurrentStep();
    }
  }
  
  // Saltar tutorial
  skipTutorial(): void {
    this.markAsSkipped();
    this.stopTutorial();
  }
  
  // Mostrar paso actual
  private showCurrentStep(): void {
    const step = this.steps[this.currentStepIndex];
    this.currentStepSubject.next(step);
  }
  
  // Obtener información del paso actual
  getCurrentStepInfo(): { current: number; total: number; step: TutorialStep | null } {
    return {
      current: this.currentStepIndex + 1,
      total: this.steps.length,
      step: this.steps[this.currentStepIndex] || null
    };
  }
  
  // Verificar si es el primer paso
  isFirstStep(): boolean {
    return this.currentStepIndex === 0;
  }
  
  // Verificar si es el último paso
  isLastStep(): boolean {
    return this.currentStepIndex === this.steps.length - 1;
  }
}

