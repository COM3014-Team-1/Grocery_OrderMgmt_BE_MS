def validate_order_data(data):
    """Validate the order creation or update data."""
    
    required_fields = ['user_id', 'total_amount', 'order_status']
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    if not isinstance(data['user_id'], str) or len(data['user_id']) != 36:
        return False, "Invalid user_id format"
    
    if not isinstance(data['total_amount'], (int, float)) or data['total_amount'] <= 0:
        return False, "Total amount must be a positive number"
    
    if not isinstance(data['order_status'], str) or data['order_status'] not in ['pending', 'shipped', 'delivered', 'cancelled']:
        return False, "Invalid order_status value. Must be one of ['pending', 'shipped', 'delivered', 'cancelled']"

    return True, ""
