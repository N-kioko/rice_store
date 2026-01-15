from domain.product import Product
from domain.sale import Sale
from domain.inventory import Inventory
from domain.customer import Customer
from domain.cart import Cart

inventory = Inventory()

rice = Product("R001", "White Rice 5kg", 600, 20, "Grains")

inventory.add_product(rice)

###  add items tocart and process sale
customer = Customer("Alice Smith", "alice@example.com", "google_id_123")
customer.cart.add_item(rice, 3)
sale = customer.cart.checkout()
total_price = sale.process_sale()
print(f"Total price for the sale: Ksh {total_price}")
inventory.remove_product(sale)
inventory.list_inventory()
