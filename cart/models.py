from django.conf import settings

from shop.models import Product


class Cart:

    def __init__(self, request):
        """Конструктор для корзины, который использует сессии"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)
                                     }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """ Сохранение данных в сессию """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """Удаление продукта из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """ Итерация по товарам """
        products = Product.objects.filter(id__in=self.cart.keys())

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = item['price']
            item['total_price'] = float(item['price']) * float(item['quantity'])
            yield item

    def item_count(self):
        """ Количество товаров """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Общая сумма товаров из корзины заказов"""
        return sum(float(item['price']) * float(item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

