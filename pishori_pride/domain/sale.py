from product import Product
class Sale:
    """ Represents a sale transaction in the store."""
    def __init__(self, product: Product, quantity: int):
        """ Initializes the Sale class with the following attributes:
        product: The product being sold
        quantity: The quantity of the product being sold"""
        self.product = product
        self.quantity = quantity
        self.price_at_sale = product.price
        self.total_price = self.price_at_sale * quantity

    def process_sale(self):
        """ Processes the sale by applying the sale on the product and calculating the total price."""
        self.product._apply_sale(self.quantity)
        return self.total_price

    def __repr__(self):
        return f"Sale(product={self.product.name}, quantity={self.quantity}, total_price={self.total_price})"