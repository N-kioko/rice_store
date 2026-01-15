from .product import Product

class Cart:
    """Represents a shopping cart for a customer"""
    def __init__(self):
        self.items = {}  # {product_sku: quantity}

    def add_item(self, product: Product, quantity: int):
        """Adds product to cart"""
        if product.sku in self.items:
            self.items[product.sku] += quantity
        else:
            self.items[product.sku] = quantity
        print(f"{quantity} units of {product.name} added to cart.")

    def remove_item(self, product: Product, quantity: int = None):
        """Removes quantity of a product or entire product from cart"""
        if product.sku in self.items:
            if quantity is None or quantity >= self.items[product.sku]:
                del self.items[product.sku]
                print(f"{product.name} removed from cart.")
            else:
                self.items[product.sku] -= quantity
                print(f"{quantity} units of {product.name} removed from cart.")
        else:
            print(f"{product.name} not in cart.")

    def view_cart(self, inventory):
        """Displays items in the cart and calculates subtotal"""
        total = 0
        print("Cart:")
        for sku, qty in self.items.items():
            product = inventory.products.get(sku)
            if product:
                subtotal = product.price * qty
                total += subtotal
                print(f"{product.name} | Qty: {qty} | Price: {product.price} | Subtotal: {subtotal}")
        print(f"Total: Ksh {total}")
        return total

    def clear_cart(self):
        """Empties the cart"""
        self.items.clear()
        print("Cart cleared.")
