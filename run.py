from app import app, db
from models import Product, Inventory, Warehouse, Supplier, SupplierProducts, Sales, ProductTypeThresholds
from datetime import datetime, timedelta

def seed_data():
    # Clear existing data if needed
    db.drop_all()
    db.create_all()

    # Add warehouse
    warehouse = Warehouse(id=1, name="Main Warehouse", company_id=1)
    db.session.add(warehouse)

    # Add product
    product = Product(id=1, name="Widget A", sku="WID-001", type="standard")
    db.session.add(product)

    # Add inventory
    inventory = Inventory(product_id=1, warehouse_id=1, quantity=5)
    db.session.add(inventory)

    # Add threshold
    threshold = ProductTypeThresholds(product_type="standard", threshold=20)
    db.session.add(threshold)

    # Add recent sale
    sale = Sales(product_id=1, warehouse_id=1, quantity=60, sale_date=datetime.utcnow() - timedelta(days=5))
    db.session.add(sale)

    # Add supplier
    supplier = Supplier(id=1, name="Supplier Corp", contact_email="orders@supplier.com")
    db.session.add(supplier)

    # Link supplier to product
    supplier_product = SupplierProducts(supplier_id=1, product_id=1)
    db.session.add(supplier_product)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        seed_data()  # Seed the data
    app.run(debug=True)
