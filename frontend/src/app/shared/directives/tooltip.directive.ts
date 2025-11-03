import { Directive, ElementRef, HostListener, Input, Renderer2, OnDestroy } from '@angular/core';

@Directive({
  selector: '[appTooltip]',
  standalone: true
})
export class TooltipDirective implements OnDestroy {
  @Input('appTooltip') tooltipText: string = '';
  @Input() tooltipPosition: 'top' | 'bottom' | 'left' | 'right' = 'top';
  
  private tooltipElement: HTMLElement | null = null;

  constructor(
    private el: ElementRef,
    private renderer: Renderer2
  ) {}

  @HostListener('mouseenter') onMouseEnter() {
    if (this.tooltipText && !this.tooltipElement) {
      this.show();
    }
  }

  @HostListener('mouseleave') onMouseLeave() {
    if (this.tooltipElement) {
      this.hide();
    }
  }

  @HostListener('focus') onFocus() {
    if (this.tooltipText && !this.tooltipElement) {
      this.show();
    }
  }

  @HostListener('blur') onBlur() {
    if (this.tooltipElement) {
      this.hide();
    }
  }

  private show(): void {
    // Crear el elemento del tooltip
    this.tooltipElement = this.renderer.createElement('div');
    this.renderer.addClass(this.tooltipElement, 'custom-tooltip');
    this.renderer.addClass(this.tooltipElement, `tooltip-${this.tooltipPosition}`);
    
    // Agregar el texto
    const text = this.renderer.createText(this.tooltipText);
    this.renderer.appendChild(this.tooltipElement, text);
    
    // Agregar al body
    this.renderer.appendChild(document.body, this.tooltipElement);
    
    // Posicionar
    this.setPosition();
    
    // Animación de entrada
    setTimeout(() => {
      if (this.tooltipElement) {
        this.renderer.addClass(this.tooltipElement, 'tooltip-show');
      }
    }, 10);
  }

  private hide(): void {
    if (this.tooltipElement) {
      this.renderer.removeClass(this.tooltipElement, 'tooltip-show');
      setTimeout(() => {
        if (this.tooltipElement) {
          this.renderer.removeChild(document.body, this.tooltipElement);
          this.tooltipElement = null;
        }
      }, 200);
    }
  }

  private setPosition(): void {
    if (!this.tooltipElement) return;
    
    const hostPos = this.el.nativeElement.getBoundingClientRect();
    const tooltipPos = this.tooltipElement.getBoundingClientRect();
    const scrollPos = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    const scrollPosX = window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0;
    
    let top = 0;
    let left = 0;
    
    switch (this.tooltipPosition) {
      case 'top':
        top = hostPos.top - tooltipPos.height - 8 + scrollPos;
        left = hostPos.left + (hostPos.width - tooltipPos.width) / 2 + scrollPosX;
        break;
      case 'bottom':
        top = hostPos.bottom + 8 + scrollPos;
        left = hostPos.left + (hostPos.width - tooltipPos.width) / 2 + scrollPosX;
        break;
      case 'left':
        top = hostPos.top + (hostPos.height - tooltipPos.height) / 2 + scrollPos;
        left = hostPos.left - tooltipPos.width - 8 + scrollPosX;
        break;
      case 'right':
        top = hostPos.top + (hostPos.height - tooltipPos.height) / 2 + scrollPos;
        left = hostPos.right + 8 + scrollPosX;
        break;
    }
    
    this.renderer.setStyle(this.tooltipElement, 'top', `${top}px`);
    this.renderer.setStyle(this.tooltipElement, 'left', `${left}px`);
  }

  ngOnDestroy(): void {
    if (this.tooltipElement) {
      this.renderer.removeChild(document.body, this.tooltipElement);
      this.tooltipElement = null;
    }
  }
}

