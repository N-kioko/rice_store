class Product:
    """ Represents a single product inthe store, i.e rice, cinamon, cloves etc"""
    def __init__(self, sku: str, name: str, price: float, stock: int, category: str):
        """the code above initializes the Product class with the following attributes:
        sku: Store Keeping Unit, a unique identifier for the product
        name; the name of the product
        price: the price of the product
        stock: the available stock quantity of the product
        price: the price of the product
        stock: the available stock quantity of the product
        category: the category of the product."""    
        self.sku = sku
        self.name = name
        self._price = price
        self._stock = stock
        self.category = category

    ## protect the price attributes
    @property
    def price(self) -> float:
        """ Returns the price of the product."""
        return self._price
    
    @price.setter
    def price(self, new_price: float):
        """ Sets a new price for the product."""
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self._price = new_price

    ## protect the stock attributes
    @property
    def stock(self) -> int:
        """ Returns the available stock of the product."""
        return self._stock
    
    ##internal method to apply sale
    def _apply_sale(self,quantity:int)->float:
        """Applies a sale by reducing the stock and calculating the total price for the given quantity."""
        if quantity > self.stock:
            raise ValueError("Insufficient stock available.")
        self._stock -= quantity
        return self._stock
    
    ##when printing the object print these details(its a representation method)
    def __repr__(self):
        return f"Product(sku={self.sku}, name={self.name}, price={self.price}, stock={self.stock}, category={self.category})"