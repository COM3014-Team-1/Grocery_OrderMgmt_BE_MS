class util:
    def get_product_ids(data):
        products=data.get('order_items',[])
        product_ids=[str(product['product_id']) for product in products]
        return product_ids