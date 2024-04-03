class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = request.session['session_key'] = {}

        self.cart = cart

    def add(self, product):
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price)}
        else:
            pass

        self.session.modified = True