from flask import current_app
 

class util:
    def get_product_ids(data):
        products=data.get('order_items',[])
        product_ids=[str(product['product_id']) for product in products]
        return product_ids
    
    def get_productId_quantity(data):
        order_items=data.get('order_items',[])
        return [ 
            {
                "product_id" : str(item['product_id']),
                "quantity"   : item['quantity']
            }
            for item in order_items
        ]
    
    def check_product_avalibility(response):
        current_app.logger.info("inside the check avalibitlity"+str(response))
        unavailableProducts = []
        for item in response:
            if not item.get("in_stock", False):
                unavailableProducts.append({
                    "product_id": item["product_id"],
                    "requested_quantity": item["requested_quantity"],
                    "available_quantity": item["available_quantity"]
                })

        return unavailableProducts
    
    def get_error_product_ids(service_response):
        return [error.get("product_id") for error in service_response.get("errors", []) if "product_id" in error]