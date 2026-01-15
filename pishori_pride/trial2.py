from domain.product import Product
from domain.sale import Sale
from domain.inventory import Inventory

rice = Product("SKU01", "Rice", 120.0, 50, "Grains")

sale1 = Sale(rice, 5)
sale1.process_sale()
sale1.__repr__()

print(rice)

rice = Product("R001", "White Rice 5kg", 600, 20, "Grains")
beans = Product("B001", "Red Beans 1kg", 150, 50, "Grains")

inventory = Inventory()
inventory.add_product(rice)
inventory.add_product(beans)

# Make a sale
sale1 = Sale(rice, 3)
sale1.process_sale()  # updates rice stock
inventory.list_inventory()

# Restock
inventory.restock("R001", 10, rice)
inventory.list_inventory()

# Check low stock
inventory.low_stock_alert(threshold=15)