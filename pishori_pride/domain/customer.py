from .cart import Cart
from .inventory import Inventory
from .payment import Payment

class Customer:
    """Represents a customer shopping online"""

    def __init__(self, name: str, email: str, google_id: str):
        self.name = name
        self.email = email
        self.google_id = google_id  # Google account identifier
        self.cart = Cart()          # Composition: customer OWNS a cart
 
    def checkout(self, inventory, payment):
        """
        Customer checks out:
        - Inventory validates stock
        - Processes sales
        - Clears cart
        - Uses the provided Payment object to pay the total amount
        """
        print(f"\n{self.name} is checking out...")
        total = 0

        if not self.cart.items:
            raise ValueError("Cart is empty. Add items before checkout.")

        # Process each item in the cart
        for sku, quantity in self.cart.items.items():
            if sku not in inventory.products:
                raise ValueError(f"Product {sku} not found in inventory")

            product = inventory.products[sku]

            if quantity > product.stock:
                raise ValueError(f"Insufficient stock for {product.name}")

            # Calculate total using product's total_cost method
            item_total = product.total_cost(quantity)

            # Process sale
            from .sale import Sale  # import here to avoid circular imports
            sale = Sale(product, quantity)
            sale.process_sale()  # reduces stock

            total += item_total
            print(f"{quantity} units of {product.name} sold for Ksh {item_total}")

        # Indicate total amount required
        print(f"Total amount required: Ksh {total}")
        # Process payment
            # Process payment
        payment.pay(total)

        # Clear cart after successful checkout
        self.cart.clear_cart()
        print(f"Checkout complete for {self.name}.\n")
        return total

    def __repr__(self):
            return f"Customer(name={self.name}, email={self.email}, google_id={self.google_id}, cart_items={len(self.cart.items)})"