"""
Servicio de integración contable - Genera asientos automáticos desde otros módulos
"""
from nest.core import Injectable
from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from datetime import datetime
from decimal import Decimal
from .accounting_repository import (
    ChartOfAccountsRepository, JournalEntryRepository, 
    AccountingPeriodRepository, GeneralLedgerRepository
)
from ...models.accounting import JournalEntryStatus, AccountType
from ...models.order import Order, OrderItem
from ...models.account_receivable import AccountReceivable, AccountReceivablePayment
from ...models.account_payable import AccountPayable, AccountPayablePayment
from ...models.product import Product


@Injectable
class AccountingIntegrationService:
    """Servicio para generar asientos contables automáticos"""
    
    def __init__(self):
        pass
    
    def get_default_accounts(self, business_id: int, db: Session) -> Dict[str, int]:
        """Obtener cuentas contables por defecto del negocio"""
        repo = ChartOfAccountsRepository(db)
        accounts = repo.find_all(business_id, active_only=True)
        
        # Buscar cuentas por código o tipo
        default_accounts = {}
        
        # Helper para comparar tipos de cuenta (ahora siempre es string)
        def account_type_matches(account, target_type):
            acc_type = account.account_type if isinstance(account.account_type, str) else account.account_type.value
            target_value = target_type.value if hasattr(target_type, 'value') else str(target_type)
            return acc_type == target_value
        
        # Cuentas de ingresos
        revenue_account = next((a for a in accounts if account_type_matches(a, AccountType.REVENUE)), None)
        if revenue_account:
            default_accounts['revenue'] = revenue_account.id
        
        # Cuentas de costo de ventas
        cost_of_sales_account = next((a for a in accounts if account_type_matches(a, AccountType.COST_OF_SALES)), None)
        if cost_of_sales_account:
            default_accounts['cost_of_sales'] = cost_of_sales_account.id
        
        # Cuentas de inventario (Activo)
        inventory_account = next((a for a in accounts if account_type_matches(a, AccountType.ASSET) and 'inventario' in a.name.lower()), None)
        if inventory_account:
            default_accounts['inventory'] = inventory_account.id
        
        # Cuentas por cobrar (Activo)
        receivables_account = next((a for a in accounts if account_type_matches(a, AccountType.ASSET) and ('cobrar' in a.name.lower() or 'receivable' in a.name.lower())), None)
        if receivables_account:
            default_accounts['accounts_receivable'] = receivables_account.id
        
        # Cuentas por pagar (Pasivo)
        payables_account = next((a for a in accounts if account_type_matches(a, AccountType.LIABILITY) and ('pagar' in a.name.lower() or 'payable' in a.name.lower())), None)
        if payables_account:
            default_accounts['accounts_payable'] = payables_account.id
        
        # Efectivo/Bancos (Activo) - Buscar "Caja" o "Bancos" primero
        cash_account = next((a for a in accounts if account_type_matches(a, AccountType.ASSET) and ('caja' in a.name.lower() or 'banco' in a.name.lower() or 'cash' in a.name.lower() or 'efectivo' in a.name.lower())), None)
        if cash_account:
            default_accounts['cash'] = cash_account.id
        
        return default_accounts
    
    def create_sale_entry(
        self,
        order: Order,
        business_id: int,
        user_id: int,
        db: Session,
        period_id: Optional[int] = None
    ) -> Optional[int]:
        """Crear asiento contable automático para una venta"""
        try:
            default_accounts = self.get_default_accounts(business_id, db)
            
            # Validar que tengamos las cuentas necesarias
            if 'revenue' not in default_accounts:
                return None  # No hay cuenta de ingresos configurada
            
            if 'cash' not in default_accounts and 'accounts_receivable' not in default_accounts:
                return None  # No hay cuenta de efectivo o cuentas por cobrar
            
            # Determinar si es venta al contado o a crédito
            # Si está pagada completamente, es al contado. Si está pendiente/parcial y tiene cliente, es a crédito
            is_credit = order.payment_status in ['pending', 'partial'] and order.customer_id is not None
            
            # Obtener período actual si no se especifica
            if not period_id:
                period_repo = AccountingPeriodRepository(db)
                current_period = period_repo.find_current(business_id)
                period_id = current_period.id if current_period else None
            
            # Calcular costo de ventas
            cost_of_sales = self._calculate_order_cost(order, db)
            
            entry_repo = JournalEntryRepository(db)
            entry_number = entry_repo.generate_entry_number(business_id)
            
            # Crear asiento
            entry = entry_repo.create({
                'business_id': business_id,
                'entry_number': entry_number,
                'entry_date': order.created_at or datetime.now(),
                'reference': f'ORD-{order.id}',
                'description': f'Venta Orden #{order.id}',
                'period_id': period_id,
                'status': 'posted',  # Contabilizar automáticamente
                'created_by': user_id,
                'posted_by': user_id,
                'posted_at': datetime.now()
            })
            
            lines = []
            
            # Línea 1: Ingresos por ventas (Crédito)
            if 'revenue' in default_accounts:
                lines.append({
                    'entry_id': entry.id,
                    'account_id': default_accounts['revenue'],
                    'debit': Decimal('0'),
                    'credit': Decimal(str(order.subtotal)),
                    'description': f'Ingresos por venta Orden #{order.id}'
                })
            
            # Línea 2: Costo de ventas (Débito) si existe cuenta
            if cost_of_sales > 0 and 'cost_of_sales' in default_accounts:
                lines.append({
                    'entry_id': entry.id,
                    'account_id': default_accounts['cost_of_sales'],
                    'debit': Decimal(str(cost_of_sales)),
                    'credit': Decimal('0'),
                    'description': f'Costo de venta Orden #{order.id}'
                })
                
                # Línea 3: Reducir inventario (Crédito)
                if 'inventory' in default_accounts:
                    lines.append({
                        'entry_id': entry.id,
                        'account_id': default_accounts['inventory'],
                        'debit': Decimal('0'),
                        'credit': Decimal(str(cost_of_sales)),
                        'description': f'Salida de inventario Orden #{order.id}'
                    })
            
            # Línea 4: Efectivo o Cuentas por cobrar
            # Si es venta a crédito (pendiente/parcial con cliente), usar cuentas por cobrar
            # Si está pagada completamente, usar efectivo
            if is_credit and 'accounts_receivable' in default_accounts:
                # Venta a crédito
                lines.append({
                    'entry_id': entry.id,
                    'account_id': default_accounts['accounts_receivable'],
                    'debit': Decimal(str(order.total)),
                    'credit': Decimal('0'),
                    'description': f'Cuenta por cobrar Orden #{order.id}'
                })
            elif 'cash' in default_accounts:
                # Venta al contado (pagada)
                lines.append({
                    'entry_id': entry.id,
                    'account_id': default_accounts['cash'],
                    'debit': Decimal(str(order.total)),
                    'credit': Decimal('0'),
                    'description': f'Ingreso en efectivo Orden #{order.id}'
                })
            
            # Crear líneas
            for line_data in lines:
                entry_repo.create_line(line_data)
            
            db.commit()
            db.refresh(entry)
            
            # Actualizar libro mayor
            ledger_repo = GeneralLedgerRepository(db)
            ledger_repo.rebuild_ledger(business_id, period_id)
            
            return entry.id
        except Exception as e:
            db.rollback()
            print(f"Error al crear asiento de venta: {str(e)}")
            return None
    
    def create_receivable_payment_entry(
        self,
        account: AccountReceivable,
        payment: AccountReceivablePayment,
        business_id: int,
        user_id: int,
        db: Session,
        period_id: Optional[int] = None
    ) -> Optional[int]:
        """Crear asiento contable automático para pago de cuenta por cobrar"""
        try:
            default_accounts = self.get_default_accounts(business_id, db)
            
            if 'accounts_receivable' not in default_accounts:
                return None
            
            if 'cash' not in default_accounts:
                return None
            
            if not period_id:
                period_repo = AccountingPeriodRepository(db)
                current_period = period_repo.find_current(business_id)
                period_id = current_period.id if current_period else None
            
            entry_repo = JournalEntryRepository(db)
            entry_number = entry_repo.generate_entry_number(business_id)
            
            entry = entry_repo.create({
                'business_id': business_id,
                'entry_number': entry_number,
                'entry_date': payment.payment_date or datetime.now(),
                'reference': f'REC-PAY-{payment.id}',
                'description': f'Pago cuenta por cobrar #{account.id}',
                'period_id': period_id,
                'status': JournalEntryStatus.POSTED,
                'created_by': user_id,
                'posted_by': user_id,
                'posted_at': datetime.now()
            })
            
            # Línea 1: Efectivo/Bancos (Débito)
            entry_repo.create_line({
                'entry_id': entry.id,
                'account_id': default_accounts['cash'],
                'debit': Decimal(str(payment.amount)),
                'credit': Decimal('0'),
                'description': f'Pago recibido cuenta #{account.id}'
            })
            
            # Línea 2: Cuentas por cobrar (Crédito)
            entry_repo.create_line({
                'entry_id': entry.id,
                'account_id': default_accounts['accounts_receivable'],
                'debit': Decimal('0'),
                'credit': Decimal(str(payment.amount)),
                'description': f'Reducción cuenta por cobrar #{account.id}'
            })
            
            db.commit()
            db.refresh(entry)
            
            # Actualizar libro mayor
            ledger_repo = GeneralLedgerRepository(db)
            ledger_repo.rebuild_ledger(business_id, period_id)
            
            return entry.id
        except Exception as e:
            db.rollback()
            print(f"Error al crear asiento de pago por cobrar: {str(e)}")
            return None
    
    def create_payable_payment_entry(
        self,
        account: AccountPayable,
        payment: AccountPayablePayment,
        business_id: int,
        user_id: int,
        db: Session,
        period_id: Optional[int] = None
    ) -> Optional[int]:
        """Crear asiento contable automático para pago de cuenta por pagar"""
        try:
            default_accounts = self.get_default_accounts(business_id, db)
            
            if 'accounts_payable' not in default_accounts:
                return None
            
            if 'cash' not in default_accounts:
                return None
            
            if not period_id:
                period_repo = AccountingPeriodRepository(db)
                current_period = period_repo.find_current(business_id)
                period_id = current_period.id if current_period else None
            
            entry_repo = JournalEntryRepository(db)
            entry_number = entry_repo.generate_entry_number(business_id)
            
            entry = entry_repo.create({
                'business_id': business_id,
                'entry_number': entry_number,
                'entry_date': payment.payment_date or datetime.now(),
                'reference': f'PAY-PAY-{payment.id}',
                'description': f'Pago cuenta por pagar #{account.id}',
                'period_id': period_id,
                'status': JournalEntryStatus.POSTED,
                'created_by': user_id,
                'posted_by': user_id,
                'posted_at': datetime.now()
            })
            
            # Línea 1: Cuentas por pagar (Débito)
            entry_repo.create_line({
                'entry_id': entry.id,
                'account_id': default_accounts['accounts_payable'],
                'debit': Decimal(str(payment.amount)),
                'credit': Decimal('0'),
                'description': f'Reducción cuenta por pagar #{account.id}'
            })
            
            # Línea 2: Efectivo/Bancos (Crédito)
            entry_repo.create_line({
                'entry_id': entry.id,
                'account_id': default_accounts['cash'],
                'debit': Decimal('0'),
                'credit': Decimal(str(payment.amount)),
                'description': f'Pago realizado cuenta #{account.id}'
            })
            
            db.commit()
            db.refresh(entry)
            
            # Actualizar libro mayor
            ledger_repo = GeneralLedgerRepository(db)
            ledger_repo.rebuild_ledger(business_id, period_id)
            
            return entry.id
        except Exception as e:
            db.rollback()
            print(f"Error al crear asiento de pago por pagar: {str(e)}")
            return None
    
    def create_purchase_entry(
        self,
        product: Product,
        quantity: float,
        total_cost: float,
        business_id: int,
        user_id: int,
        db: Session,
        is_credit: bool = False,
        period_id: Optional[int] = None
    ) -> Optional[int]:
        """Crear asiento contable automático para compra de inventario"""
        try:
            default_accounts = self.get_default_accounts(business_id, db)
            
            if 'inventory' not in default_accounts:
                return None
            
            if is_credit and 'accounts_payable' not in default_accounts:
                return None
            
            if not is_credit and 'cash' not in default_accounts:
                return None
            
            if not period_id:
                period_repo = AccountingPeriodRepository(db)
                current_period = period_repo.find_current(business_id)
                period_id = current_period.id if current_period else None
            
            entry_repo = JournalEntryRepository(db)
            entry_number = entry_repo.generate_entry_number(business_id)
            
            entry = entry_repo.create({
                'business_id': business_id,
                'entry_number': entry_number,
                'entry_date': datetime.now(),
                'reference': f'PURCH-{product.id}',
                'description': f'Compra de inventario: {product.name}',
                'period_id': period_id,
                'status': JournalEntryStatus.POSTED,
                'created_by': user_id,
                'posted_by': user_id,
                'posted_at': datetime.now()
            })
            
            # Línea 1: Inventario (Débito)
            entry_repo.create_line({
                'entry_id': entry.id,
                'account_id': default_accounts['inventory'],
                'debit': Decimal(str(total_cost)),
                'credit': Decimal('0'),
                'description': f'Entrada de inventario: {product.name}'
            })
            
            # Línea 2: Cuentas por pagar o Efectivo (Crédito)
            if is_credit:
                entry_repo.create_line({
                    'entry_id': entry.id,
                    'account_id': default_accounts['accounts_payable'],
                    'debit': Decimal('0'),
                    'credit': Decimal(str(total_cost)),
                    'description': f'Cuenta por pagar compra: {product.name}'
                })
            else:
                entry_repo.create_line({
                    'entry_id': entry.id,
                    'account_id': default_accounts['cash'],
                    'debit': Decimal('0'),
                    'credit': Decimal(str(total_cost)),
                    'description': f'Pago compra: {product.name}'
                })
            
            db.commit()
            db.refresh(entry)
            
            # Actualizar libro mayor
            ledger_repo = GeneralLedgerRepository(db)
            ledger_repo.rebuild_ledger(business_id, period_id)
            
            return entry.id
        except Exception as e:
            db.rollback()
            print(f"Error al crear asiento de compra: {str(e)}")
            return None
    
    def _calculate_order_cost(self, order: Order, db: Session) -> float:
        """Calcular el costo de ventas de una orden"""
        total_cost = 0.0
        
        for item in order.items:
            if item.source_type == 'product' and item.product_id:
                # Obtener producto
                from ...nest_modules.orders.orders_repository import ProductRepository
                product_repo = ProductRepository(db)
                product = product_repo.find_by_id(item.product_id, order.business_id)
                if product:
                    total_cost += product.purchase_price * item.quantity
            elif item.source_type == 'menu' and item.menu_item_id:
                # Calcular costo del menú basado en ingredientes
                from ...models.menu import MenuItem, menu_item_ingredients
                from sqlalchemy.orm import joinedload
                
                menu_item = db.query(MenuItem).options(
                    joinedload(MenuItem.ingredients)
                ).filter(MenuItem.id == item.menu_item_id).first()
                
                if menu_item and menu_item.ingredients:
                    for ingredient in menu_item.ingredients:
                        if ingredient.product:
                            total_cost += ingredient.product.purchase_price * ingredient.quantity * item.quantity
        
        return total_cost

