class OrderNotFoundError(Exception):
    """Raised when an order is not found."""
    pass

class OrderCreationError(Exception):
    """Raised when there is an error creating an order."""
    pass

class OrderUpdateError(Exception):
    """Raised when there is an error updating an order."""
    pass

class OrderCancelError(Exception):
    """Raised when there is an error canceling an order."""
    pass

class UserOrdersFetchError(Exception):
    """Raised when there is an error fetching user orders."""
    pass

class CartItemNotFoundError(Exception):
    """Raised when a cart item is not found."""
    pass

class CartAddError(Exception):
    """Raised when there is an error adding to the cart."""
    pass

class CartRemoveError(Exception):
    """Raised when there is an error removing from the cart."""
    pass

class CartUpdateError(Exception):
    """Raised when there is an error updating the cart."""
    pass

class CartFetchError(Exception):
    """Raised when there is an error fetching cart items."""
    pass