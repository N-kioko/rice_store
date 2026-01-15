from .payment import Payment

class Cash(Payment):
    def __init__(self, currency="Ksh"):
        self.currency = currency

    def pay(self, amount: float):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        print(f"Payment of {self.currency} {amount} received in cash.")
        return True

    def refund(self, amount: float):
        if amount <= 0:
            raise ValueError("Refund amount must be greater than zero.")
        print(f"Refund of {self.currency} {amount} processed.")
        return True
