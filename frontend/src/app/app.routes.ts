import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent)
  },
  {
    path: 'cashier-pos',
    canActivate: [authGuard],
    loadComponent: () => import('./features/cashier-pos/cashier-pos.component').then(m => m.CashierPosComponent)
  },
  {
    path: 'catalog/:slug',
    loadComponent: () => import('./features/public-catalog/public-catalog.component').then(m => m.PublicCatalogComponent)
  },
  {
    path: '',
    canActivate: [authGuard],
    loadComponent: () => import('./features/layout/layout.component').then(m => m.LayoutComponent),
    children: [
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      },
      {
        path: 'dashboard',
        loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent)
      },
      {
        path: 'inventory',
        loadComponent: () => import('./features/inventory/inventory.component').then(m => m.InventoryComponent)
      },
      {
        path: 'menu',
        loadComponent: () => import('./features/menu/menu.component').then(m => m.MenuComponent)
      },
      {
        path: 'tables',
        loadComponent: () => import('./features/tables/tables.component').then(m => m.TablesComponent)
      },
      {
        path: 'orders',
        loadComponent: () => import('./features/orders/orders.component').then(m => m.OrdersComponent)
      },
      {
        path: 'users',
        loadComponent: () => import('./features/users/users.component').then(m => m.UsersComponent)
      },
      {
        path: 'customers',
        loadComponent: () => import('./features/customers/customers.component').then(m => m.CustomersComponent)
      },
      {
        path: 'cash-closing',
        loadComponent: () => import('./features/cash-closing/cash-closing.component').then(m => m.CashClosingComponent)
      },
      {
        path: 'accounts-receivable',
        loadComponent: () => import('./features/accounts-receivable/accounts-receivable.component').then(m => m.AccountsReceivableComponent)
      },
      {
        path: 'accounts-payable',
        loadComponent: () => import('./features/accounts-payable/accounts-payable.component').then(m => m.AccountsPayableComponent)
      },
      {
        path: 'accounting',
        loadComponent: () => import('./features/accounting/accounting.component').then(m => m.AccountingComponent),
        children: [
          {
            path: '',
            redirectTo: 'chart-of-accounts',
            pathMatch: 'full'
          },
          {
            path: 'chart-of-accounts',
            loadComponent: () => import('./features/accounting/chart-of-accounts/chart-of-accounts.component').then(m => m.ChartOfAccountsComponent)
          },
          {
            path: 'journal-entries',
            loadComponent: () => import('./features/accounting/journal-entries/journal-entries.component').then(m => m.JournalEntriesComponent)
          },
          {
            path: 'general-ledger',
            loadComponent: () => import('./features/accounting/general-ledger/general-ledger.component').then(m => m.GeneralLedgerComponent)
          },
          {
            path: 'trial-balance',
            loadComponent: () => import('./features/accounting/trial-balance/trial-balance.component').then(m => m.TrialBalanceComponent)
          },
          {
            path: 'financial-statements',
            loadComponent: () => import('./features/accounting/financial-statements/financial-statements.component').then(m => m.FinancialStatementsComponent)
          },
          {
            path: 'periods',
            loadComponent: () => import('./features/accounting/periods/periods.component').then(m => m.PeriodsComponent)
          }
        ]
      },
      {
        path: 'statistics/general',
        loadComponent: () => import('./features/statistics/general/statistics-general.component').then(m => m.StatisticsGeneralComponent)
      },
      {
        path: 'statistics/best-sellers',
        loadComponent: () => import('./features/statistics/best-sellers/statistics-best-sellers.component').then(m => m.StatisticsBestSellersComponent)
      },
      {
        path: 'statistics/customers',
        loadComponent: () => import('./features/statistics/customers/statistics-customers.component').then(m => m.StatisticsCustomersComponent)
      },
      {
        path: 'statistics/financial',
        loadComponent: () => import('./features/statistics/financial/statistics-financial.component').then(m => m.StatisticsFinancialComponent)
      },
      {
        path: 'statistics',
        redirectTo: 'statistics/general',
        pathMatch: 'full'
      },
      {
        path: 'profile',
        loadComponent: () => import('./features/profile/profile.component').then(m => m.ProfileComponent)
      },
      {
        path: 'configuration/business',
        loadComponent: () => import('./features/configuration/configuration.component').then(m => m.ConfigurationComponent)
      },
      {
        path: 'configuration/roles',
        loadComponent: () => import('./features/roles-permissions/roles-permissions.component').then(m => m.RolesPermissionsComponent)
      },
      {
        path: 'configuration',
        redirectTo: 'configuration/business',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '**',
    redirectTo: 'dashboard'
  }
];

