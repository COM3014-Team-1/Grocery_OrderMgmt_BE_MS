from marshmallow import ValidationError
from decimal import Decimal

class validator:
    def validate_order_data(data):
        """Validate the order creation or update data."""
        required_fields = ['order_status']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
            
        if not isinstance(data['order_status'], str) or data['order_status'] not in ['pending', 'shipped', 'delivered', 'cancelled']:
            return False, "Invalid order_status value. Must be one of ['pending', 'shipped', 'delivered', 'cancelled']"

        return True, ""
    
    def validate_Update_fields(data):
        if "order_status" not in data:
            raise ValidationError("order_status is required during update.", "order_status")

        if data.get("order_status") not in ["pending", "shipped", "delivered", "cancelled"]:
            raise ValidationError("Invalid value for order_status. Must be one of 'Pending', 'Shipped', 'Delivered', or 'Cancelled'.", "order_status")
        
        if "user_id" not in data:
            raise ValidationError("user_id is required during update.", "user_id")
        
    def validate_unit_price(value):
        """Custom validation for unit price."""
        if value <= 0:
            raise ValidationError("Unit price must be greater than zero.")
        return value

    def validate_quantity(value):
        """Custom validation for quantity."""
        if value <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return value

    def compute_subtotal(self, data, **kwargs):
        """Compute subtotal based on quantity and unit_price."""
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')
        if quantity and unit_price:
            data['subtotal'] = str(Decimal(quantity) * Decimal(unit_price))
        return data

    def compute_subtotal(self, data, **kwargs):
        """Compute subtotal on update if quantity is changed."""
        quantity = data.get('quantity')
        if quantity:
            data['subtotal'] = str(Decimal(quantity) * Decimal(data.get('unit_price')))
        return data
            
