from cart import Cart

class Customer:
    """Represents a customer shopping online"""

    def __init__(self, name: str, email: str, google_id: str):
        self.name = name
        self.email = email
        self.google_id = google_id  # Google account identifier
        self.cart = Cart()          # Composition: customer OWNS a cart

    def __repr__(self):
        return f"Customer(name={self.name}, email={self.email}, google_id={self.google_id})"