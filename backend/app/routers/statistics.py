from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models.user import User
from ..models.order import Order, OrderItem
from ..models.order_payment import OrderPayment
from ..models.payment_method import PaymentMethod
from ..models.customer import Customer
from ..models.account_receivable import AccountReceivable
from ..models.account_payable import AccountPayable
from ..models.product import Product
from ..models.menu import MenuItem
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/general")
def get_general_statistics(
    days: int = Query(30, description="Número de días para análisis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Estadísticas generales del negocio"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Órdenes del período
    orders = db.query(Order).filter(
        Order.user_id.in_(
            db.query(User.id).filter(User.business_id == current_user.business_id)
        ),
        Order.created_at >= start_date
    ).all()
    
    # Calcular métricas
    total_orders = len(orders)
    completed_orders = len([o for o in orders if o.status == 'completed'])
    cancelled_orders = len([o for o in orders if o.status == 'cancelled'])
    
    paid_orders = [o for o in orders if o.payment_status == 'paid']
    total_revenue = sum(o.total for o in paid_orders)
    average_ticket = total_revenue / len(paid_orders) if paid_orders else 0
    
    # Órdenes por día
    orders_by_day = {}
    revenue_by_day = {}
    
    for order in paid_orders:
        date_key = order.created_at.strftime('%Y-%m-%d')
        orders_by_day[date_key] = orders_by_day.get(date_key, 0) + 1
        revenue_by_day[date_key] = revenue_by_day.get(date_key, 0) + order.total
    
    # Cuentas por cobrar/pagar
    receivables = db.query(AccountReceivable).filter(
        AccountReceivable.business_id == current_user.business_id,
        AccountReceivable.deleted_at.is_(None)
    ).all()
    
    payables = db.query(AccountPayable).filter(
        AccountPayable.business_id == current_user.business_id,
        AccountPayable.deleted_at.is_(None)
    ).all()
    
    total_receivable = sum(acc.amount_pending for acc in receivables)
    total_payable = sum(acc.amount_pending for acc in payables)
    
    return {
        "period_days": days,
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "total_revenue": round(total_revenue, 2),
        "average_ticket": round(average_ticket, 2),
        "orders_by_day": orders_by_day,
        "revenue_by_day": revenue_by_day,
        "total_receivable": round(total_receivable, 2),
        "total_payable": round(total_payable, 2),
        "net_balance": round(total_revenue + total_receivable - total_payable, 2)
    }


@router.get("/best-sellers")
def get_best_sellers(
    days: int = Query(30, description="Número de días para análisis"),
    limit: int = Query(10, description="Cantidad de resultados"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Productos y platos más vendidos"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Obtener órdenes del período
    orders = db.query(Order).filter(
        Order.user_id.in_(
            db.query(User.id).filter(User.business_id == current_user.business_id)
        ),
        Order.created_at >= start_date
    ).all()
    
    order_ids = [o.id for o in orders]
    
    # Productos más vendidos
    product_sales = db.query(
        Product.id,
        Product.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.subtotal).label('total_sales')
    ).join(
        OrderItem, OrderItem.product_id == Product.id
    ).filter(
        OrderItem.order_id.in_(order_ids),
        OrderItem.product_id.isnot(None)
    ).group_by(
        Product.id, Product.name
    ).order_by(
        desc('total_quantity')
    ).limit(limit).all()
    
    # Ítems de menú más vendidos
    menu_sales = db.query(
        MenuItem.id,
        MenuItem.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.subtotal).label('total_sales')
    ).join(
        OrderItem, OrderItem.menu_item_id == MenuItem.id
    ).filter(
        OrderItem.order_id.in_(order_ids),
        OrderItem.menu_item_id.isnot(None)
    ).group_by(
        MenuItem.id, MenuItem.name
    ).order_by(
        desc('total_quantity')
    ).limit(limit).all()
    
    # Productos menos vendidos (solo los que se han vendido al menos una vez)
    worst_products = db.query(
        Product.id,
        Product.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.subtotal).label('total_sales')
    ).join(
        OrderItem, OrderItem.product_id == Product.id
    ).filter(
        OrderItem.order_id.in_(order_ids),
        OrderItem.product_id.isnot(None)
    ).group_by(
        Product.id, Product.name
    ).order_by(
        'total_quantity'
    ).limit(limit).all()
    
    return {
        "period_days": days,
        "best_products": [
            {
                "id": p.id,
                "name": p.name,
                "quantity": int(p.total_quantity),
                "total_sales": round(float(p.total_sales), 2)
            }
            for p in product_sales
        ],
        "best_menu_items": [
            {
                "id": m.id,
                "name": m.name,
                "quantity": int(m.total_quantity),
                "total_sales": round(float(m.total_sales), 2)
            }
            for m in menu_sales
        ],
        "worst_products": [
            {
                "id": p.id,
                "name": p.name,
                "quantity": int(p.total_quantity),
                "total_sales": round(float(p.total_sales), 2)
            }
            for p in worst_products
        ]
    }


@router.get("/customers")
def get_customer_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Estadísticas de clientes"""
    
    # Total de clientes
    total_customers = db.query(Customer).filter(
        Customer.business_id == current_user.business_id,
        Customer.deleted_at.is_(None)
    ).count()
    
    # Clientes nuevos en últimos 30 días
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_customers = db.query(Customer).filter(
        Customer.business_id == current_user.business_id,
        Customer.deleted_at.is_(None),
        Customer.created_at >= thirty_days_ago
    ).count()
    
    # Cuentas por cobrar por cliente
    receivables = db.query(
        Customer.id,
        Customer.nombre,
        Customer.apellido,
        func.count(AccountReceivable.id).label('accounts_count'),
        func.sum(AccountReceivable.amount_pending).label('total_pending')
    ).join(
        AccountReceivable, AccountReceivable.customer_id == Customer.id
    ).filter(
        Customer.business_id == current_user.business_id,
        Customer.deleted_at.is_(None),
        AccountReceivable.deleted_at.is_(None),
        AccountReceivable.status.in_(['pending', 'partial', 'overdue'])
    ).group_by(
        Customer.id, Customer.nombre, Customer.apellido
    ).order_by(
        desc('total_pending')
    ).limit(10).all()
    
    customers_with_debt = [
        {
            "id": r.id,
            "name": f"{r.nombre} {r.apellido or ''}".strip(),
            "accounts_count": r.accounts_count,
            "total_pending": round(float(r.total_pending or 0), 2)
        }
        for r in receivables
    ]
    
    return {
        "total_customers": total_customers,
        "new_customers_last_30_days": new_customers,
        "customers_with_debt": customers_with_debt,
        "total_debt_from_customers": round(sum(c['total_pending'] for c in customers_with_debt), 2)
    }


@router.get("/financial")
def get_financial_statistics(
    days: int = Query(30, description="Número de días para análisis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Estadísticas de ingresos y egresos"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Ingresos (órdenes pagadas) - cargar pagos y métodos de pago
    orders = db.query(Order).options(
        joinedload(Order.payments).joinedload(OrderPayment.payment_method)
    ).filter(
        Order.user_id.in_(
            db.query(User.id).filter(User.business_id == current_user.business_id)
        ),
        Order.payment_status == 'paid',
        Order.created_at >= start_date
    ).all()
    
    total_income = sum(o.total for o in orders)
    
    # Ingresos por método de pago (aproximado usando order.payments)
    income_by_method = {}
    for order in orders:
        if order.payments:
            for payment in order.payments:
                # Acceder al nombre del método de pago a través de la relación
                method_name = payment.payment_method.name if payment.payment_method else 'Otro'
                income_by_method[method_name] = income_by_method.get(method_name, 0) + payment.amount
    
    # Egresos (cuentas por pagar pagadas en el período)
    payables = db.query(AccountPayable).filter(
        AccountPayable.business_id == current_user.business_id,
        AccountPayable.deleted_at.is_(None),
        AccountPayable.updated_at >= start_date,
        AccountPayable.amount_paid > 0
    ).all()
    
    total_expenses = sum(p.amount_paid for p in payables)
    
    # Egresos pendientes
    pending_expenses = db.query(AccountPayable).filter(
        AccountPayable.business_id == current_user.business_id,
        AccountPayable.deleted_at.is_(None),
        AccountPayable.status.in_(['pending', 'partial', 'overdue'])
    ).all()
    
    total_pending_expenses = sum(p.amount_pending for p in pending_expenses)
    
    # Ingresos pendientes
    receivables = db.query(AccountReceivable).filter(
        AccountReceivable.business_id == current_user.business_id,
        AccountReceivable.deleted_at.is_(None),
        AccountReceivable.status.in_(['pending', 'partial', 'overdue'])
    ).all()
    
    total_pending_income = sum(r.amount_pending for r in receivables)
    
    # Calcular balance
    net_profit = total_income - total_expenses
    projected_balance = net_profit + total_pending_income - total_pending_expenses
    
    return {
        "period_days": days,
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_profit": round(net_profit, 2),
        "income_by_method": {k: round(v, 2) for k, v in income_by_method.items()},
        "total_pending_income": round(total_pending_income, 2),
        "total_pending_expenses": round(total_pending_expenses, 2),
        "projected_balance": round(projected_balance, 2),
        "profit_margin": round((net_profit / total_income * 100) if total_income > 0 else 0, 2)
    }

