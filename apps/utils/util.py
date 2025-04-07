class util:
    def get_product_ids(data):
        products=data.get('order_products',[])
        product_ids=[products['product_id'] for product in products]
        return product_ids