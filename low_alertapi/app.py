from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta
from models import OrderItems, Orders, Product, Warehouse, Inventory, Supplier

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route("/api/companies/<int:company_id>/alerts/low-stock", methods=["GET"])
def low_stock_alerts(company_id):

    alerts = []

    # only recent sales (last 30 days)
    cutoff = datetime.now() - timedelta(days=30)

    # sales per product (recent)
    sales_query = (
        db.session.query(
            OrderItems.product_id,
            func.sum(OrderItems.quantity).label("total_sold")
        )
        .join(Orders, Orders.id == OrderItems.order_id)
        .filter(Orders.order_date >= cutoff)
        .group_by(OrderItems.product_id)
        .subquery()
    )

    query = (
        db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            Warehouse.id,
            Warehouse.name,
            Inventory.current_stock,
            Inventory.threshold,
            Supplier.id,
            Supplier.name,
            Supplier.email,
            sales_subq.c.total_sold
        )
        .join(Inventory, Inventory.product_id == Product.id)
        .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
        .join(Supplier, Supplier.id == Product.supplier_id)
        .join(
            sales_subq,
            sales_subq.c.product_id == Product.id
        )
        .filter(Warehouse.company_id == company_id)
        .filter(Inventory.current_stock <= Inventory.threshold)
    )

    results = query.all()

    for row in results:

        (
            product_id,
            product_name,
            sku,
            warehouse_id,
            warehouse_name,
            current_stock,
            threshold,
            supplier_id,
            supplier_name,
            supplier_email,
            total_sold
        ) = row

        # avg daily sales (30 days)
        avg_daily_sales = total_sold / 30 if total_sold else 0

        if avg_daily_sales == 0:
            continue

        days_until_stockout = int(current_stock / avg_daily_sales)

        alerts.append({
            "product_id": product_id,
            "product_name": product_name,
            "sku": sku,
            "warehouse_id": warehouse_id,
            "warehouse_name": warehouse_name,
            "current_stock": current_stock,
            "threshold": threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": {
                "id": supplier_id,
                "name": supplier_name,
                "contact_email": supplier_email
            }
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })

if __name__ == '__main__':
    app.run()
