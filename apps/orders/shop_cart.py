from apps.products.models import Product


class ShopCart:
    def __init__(self, request):
        self.session = request.session
        shop_cart = self.session.get('shop_cart')
        if not shop_cart:
            shop_cart = self.session['shop_cart'] = {}
        self.shop_cart = shop_cart
        self.count = len(self.shop_cart)
    
    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id] = {'qty':0, 'price':product.price, }#'discounted_price':product.get_discounted_price()}
        self.shop_cart[product_id]['qty'] += int(quantity)
        self.count = len(self.shop_cart)
        self.save()
    
    def save(self):
        self.session.modified = True

    def delete(self, product_id):
        del self.shop_cart[product_id]
        self.save()
    
    def update(self, product_id_list, qty_list):
        for i in range (len(product_id_list)):
            product_id = product_id_list[i]
            qty = int(qty_list[i])
            self.shop_cart[product_id]['qty'] = qty
        self.save()
        
    def __iter__(self):
        id_list = self.shop_cart.keys()
        products = Product.objects.filter(id__in=id_list, is_active=True)
        shop_cart = self.shop_cart.copy()

        for product in products:
            shop_cart[str(product.id)]['product'] = product
            
        for value in shop_cart.values():
            value['total_price']  =  value['price'] * value['qty']
            yield value

    def calc_total_price(self):
        sum = 0
        for item in self:
            sum += item['total_price']
        return sum 