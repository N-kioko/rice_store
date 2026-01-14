from domain.product import Product
from domain.sale import Sale

rice = Product("SKU01", "Rice", 120.0, 50, "Grains")

sale1 = Sale(rice, 5)
sale1.process_sale()
sale1.__repr__()

print(rice)

