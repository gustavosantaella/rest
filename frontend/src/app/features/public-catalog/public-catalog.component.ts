import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { PublicService, BusinessInfo } from '../../core/services/public.service';
import { UploadService } from '../../core/services/upload.service';
import { Product } from '../../core/models/product.model';
import { MenuItem, MenuCategory } from '../../core/models/menu.model';

@Component({
  selector: 'app-public-catalog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './public-catalog.component.html',
  styleUrls: ['./public-catalog.component.scss']
})
export class PublicCatalogComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private publicService = inject(PublicService);
  public uploadService = inject(UploadService);

  slug: string = '';
  businessInfo: BusinessInfo | null = null;
  products: Product[] = [];
  menuItems: MenuItem[] = [];
  menuCategories: MenuCategory[] = [];
  loading = true;
  error = false;
  
  activeTab: 'menu' | 'products' = 'menu';
  
  showDetailModal = false;
  selectedItem: any = null;
  loadingDetail = false;
  logoError = false;

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.slug = params['slug'];
      this.loadCatalog();
    });
  }

  loadCatalog(): void {
    this.loading = true;
    this.error = false;
    this.logoError = false; // Reset logo error when loading new catalog

    this.publicService.getBusinessInfo(this.slug).subscribe({
      next: (info) => {
        this.businessInfo = info;
        this.loadProducts();
        this.loadMenu();
      },
      error: () => {
        this.error = true;
        this.loading = false;
      }
    });
  }

  loadProducts(): void {
    this.publicService.getProducts(this.slug).subscribe({
      next: (products) => {
        this.products = products;
        this.checkLoadingComplete();
      },
      error: () => {
        this.checkLoadingComplete();
      }
    });
  }

  loadMenu(): void {
    this.publicService.getMenu(this.slug).subscribe({
      next: (menu) => {
        this.menuItems = menu;
        this.loadMenuCategories();
      },
      error: () => {
        this.checkLoadingComplete();
      }
    });
  }

  loadMenuCategories(): void {
    this.publicService.getMenuCategories(this.slug).subscribe({
      next: (categories) => {
        this.menuCategories = categories;
        this.checkLoadingComplete();
      },
      error: () => {
        this.checkLoadingComplete();
      }
    });
  }

  checkLoadingComplete(): void {
    this.loading = false;
  }

  getMenuItemsByCategory(categoryId: number): MenuItem[] {
    return this.menuItems.filter(item => item.category_id === categoryId);
  }

  onImageError(event: Event): void {
    const img = event.target as HTMLImageElement;
    img.src = 'https://via.placeholder.com/400x300?text=Sin+Imagen';
  }

  openItemDetail(itemId: number): void {
    this.loadingDetail = true;
    this.showDetailModal = true;
    this.selectedItem = null;

    this.publicService.getMenuItemDetail(this.slug, itemId).subscribe({
      next: (item) => {
        this.selectedItem = item;
        this.loadingDetail = false;
      },
      error: () => {
        this.loadingDetail = false;
        this.closeDetailModal();
      }
    });
  }

  closeDetailModal(): void {
    this.showDetailModal = false;
    this.selectedItem = null;
  }

  onLogoError(): void {
    this.logoError = true;
  }

  getUnitLabel(unitType: string): string {
    const labels: any = {
      'unit': 'unidad(es)',
      'weight_gram': 'g',
      'weight_kg': 'kg',
      'volume_ml': 'ml',
      'volume_l': 'L',
      'bulk': 'a granel'
    };
    return labels[unitType] || '';
  }
}

