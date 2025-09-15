from flask import Flask, jsonify
from datetime import datetime, timedelta
from models import db, Product, Inventory, Warehouse, Supplier, SupplierProducts, Sales, ProductTypeThresholds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    recent_sales_cutoff = datetime.utcnow() - timedelta(days=30)

    warehouses = Warehouse.query.filter_by(company_id=company_id).all()
    if not warehouses:
        return jsonify({"alerts": [], "total_alerts": 0})

    alerts = []
    inventories = db.session.query(Inventory, Product, Warehouse).join(
        Product, Inventory.product_id == Product.id
    ).join(
        Warehouse, Inventory.warehouse_id == Warehouse.id
    ).filter(
        Warehouse.company_id == company_id
    ).all()

    for inventory, product, warehouse in inventories:
        threshold_entry = ProductTypeThresholds.query.filter_by(product_type=product.type).first()
        threshold = threshold_entry.threshold if threshold_entry else 10

        if inventory.quantity >= threshold:
            continue

        recent_sales = db.session.query(db.func.sum(Sales.quantity)).filter(
            Sales.product_id == product.id,
            Sales.warehouse_id == warehouse.id,
            Sales.sale_date >= recent_sales_cutoff
        ).scalar() or 0

        if recent_sales == 0:
            continue

        avg_daily_sales = recent_sales / 30
        days_until_stockout = round(inventory.quantity / avg_daily_sales) if avg_daily_sales > 0 else None

        supplier_relation = SupplierProducts.query.filter_by(product_id=product.id).first()
        if supplier_relation:
            supplier = Supplier.query.get(supplier_relation.supplier_id)
            supplier_info = {
                "id": supplier.id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            }
        else:
            supplier_info = {
                "id": None,
                "name": "Unknown",
                "contact_email": None
            }

        alert = {
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "current_stock": inventory.quantity,
            "threshold": threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": supplier_info
        }
        alerts.append(alert)

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })
