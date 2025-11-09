import { Component, OnInit, OnDestroy, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TutorialService, TutorialStep } from '../../../core/services/tutorial.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-tutorial',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tutorial.component.html',
  styleUrls: ['./tutorial.component.scss']
})
export class TutorialComponent implements OnInit, OnDestroy {
  private tutorialService = inject(TutorialService);
  private cdr = inject(ChangeDetectorRef);
  
  isActive = false;
  currentStep: TutorialStep | null = null;
  stepInfo = { current: 1, total: 1 };
  
  highlightedElement: HTMLElement | null = null;
  tooltipPosition = { top: '50%', left: '50%' };
  
  private subscriptions: Subscription[] = [];
  
  ngOnInit(): void {
    // Suscribirse al estado del tutorial
    this.subscriptions.push(
      this.tutorialService.isActive$.subscribe(isActive => {
        this.isActive = isActive;
        if (!isActive) {
          this.removeHighlight();
        }
        this.cdr.detectChanges();
      })
    );
    
    // Suscribirse al paso actual
    this.subscriptions.push(
      this.tutorialService.currentStep$.subscribe(step => {
        this.currentStep = step;
        this.stepInfo = this.tutorialService.getCurrentStepInfo();
        
        if (step && step.element) {
          setTimeout(() => this.highlightElement(step.element), 100);
        } else {
          this.removeHighlight();
        }
        
        this.cdr.detectChanges();
      })
    );
  }
  
  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
    this.removeHighlight();
  }
  
  highlightElement(selector: string): void {
    this.removeHighlight();
    
    const element = document.querySelector(selector) as HTMLElement;
    if (element) {
      this.highlightedElement = element;
      element.classList.add('tutorial-highlight');
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
      // Calcular posición del tooltip
      this.calculateTooltipPosition(element);
    }
  }
  
  removeHighlight(): void {
    if (this.highlightedElement) {
      this.highlightedElement.classList.remove('tutorial-highlight');
      this.highlightedElement = null;
    }
  }
  
  calculateTooltipPosition(element: HTMLElement): void {
    const rect = element.getBoundingClientRect();
    const position = this.currentStep?.position || 'right';
    
    switch (position) {
      case 'right':
        this.tooltipPosition = {
          top: `${rect.top + rect.height / 2}px`,
          left: `${rect.right + 20}px`
        };
        break;
      case 'left':
        this.tooltipPosition = {
          top: `${rect.top + rect.height / 2}px`,
          left: `${rect.left - 320}px` // 300px ancho tooltip + 20px margen
        };
        break;
      case 'top':
        this.tooltipPosition = {
          top: `${rect.top - 180}px`, // Altura aproximada del tooltip
          left: `${rect.left + rect.width / 2}px`
        };
        break;
      case 'bottom':
        this.tooltipPosition = {
          top: `${rect.bottom + 20}px`,
          left: `${rect.left + rect.width / 2}px`
        };
        break;
      case 'center':
      default:
        this.tooltipPosition = {
          top: '50%',
          left: '50%'
        };
    }
  }
  
  onNext(): void {
    this.tutorialService.nextStep();
  }
  
  onPrevious(): void {
    this.tutorialService.previousStep();
  }
  
  onSkip(): void {
    this.tutorialService.skipTutorial();
  }
  
  isFirstStep(): boolean {
    return this.tutorialService.isFirstStep();
  }
  
  isLastStep(): boolean {
    return this.tutorialService.isLastStep();
  }
  
  isCenterPosition(): boolean {
    return this.currentStep?.position === 'center' || !this.currentStep?.element;
  }
}

