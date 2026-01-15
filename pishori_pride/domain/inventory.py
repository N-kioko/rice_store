from .product import Product
from .sale import Sale

class Inventory:
    """this manages the collection of products in the store."""
    def __init__(self):
        self.products = {}
    
    def add_product(self, product: Product):
        """Adds a new product to the inventory.
            If the product already exists, updates its stock instead.
         """
        if product.sku in self.products:
            # Product exists → just restock
            self.products[product.sku]._stock += product.stock  # directly update _stock
            print(f"{product.name} restocked by {product.stock}. New stock: {self.products[product.sku].stock}")
        else:
            # New product → add to inventory
            self.products[product.sku] = product
            print(f"Product {product.name} added to inventory.")

    def restock(self, sku: str, quantity: int, product: Product):
        if sku in self.products:
            product = self.products[sku]
            product._stock += quantity
            print(f"{product.name} restocked by {quantity}. New stock: {product.stock}")
        else:
            raise ValueError("Product not found in inventory.")
        
    def remove_product(self, sale: Sale):
        """ Removes a product from the inventory after sale in units sold."""
        if sale.sku in self.products:
             product=self.products[sale.sku]
             product._apply_sale(sale.quantity)
             print(f"{sale.quantity} units of {product.name} sold.")
        else:
            raise ValueError("Product with this SKU does not exist.")
        
    def check_stock(self, sku: str) -> int:
        """ Returns the current stock for a given product """
        if sku in self.products:
            return self.products[sku].stock
        return 0
    
    def list_inventory(self):
        """ Prints all products and their stock """
        print("Current Inventory:")
        for product in self.products.values():
            print(f"{product.name} | SKU: {product.sku} | Stock: {product.stock} | Price: Ksh {product.price} | Category: {product.category}")

    def low_stock_alert(self, threshold: int = 5):
        """ Lists products with stock below a threshold """
        low_stock = [p for p in self.products.values() if p.stock <= threshold]
        if low_stock:
            print("Low stock products:")
            for p in low_stock:
                print(f"{p.name} | Stock: {p.stock}")
        else:
            print("All products are sufficiently stocked.")