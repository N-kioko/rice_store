from domain.product import Product
from domain.sale import Sale
from domain.inventory import Inventory
from domain.customer import Customer
from domain.cart import Cart

inventory = Inventory()

rice = Product("R001", "White Rice 5kg", 600, 20, "Grains")

inventory.add_product(rice)
