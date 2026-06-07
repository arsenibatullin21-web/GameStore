import copy
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings

from main.models import Product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'product_id': int(product_id),
                'price': str(product.final_price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = 1
        else:
            self.cart[product_id]['quantity'] += 1

        self.save()

    def delete(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear_items(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def update_quantity(self, product_id, action):
        if product_id in self.cart:
            if action == 'increase':
                self.cart[product_id]['quantity'] += 1
            elif action == 'decrease':
                self.cart[product_id]['quantity'] -= 1
                if self.cart[product_id]['quantity'] <= 0:
                    del self.cart[product_id]
        self.save()

    def get_total(self, promo=None):
        total = Decimal('0.00')

        for item in self.cart.values():
            total += Decimal(item['price']) * Decimal(item['quantity'])

        if promo:
            discount_amount = total * Decimal(promo.discount) / Decimal("100")
            total = (total - discount_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return total

    def __iter__(self):
        product_ids = [
            item['product_id']
            for item in self.cart.values()
        ]

        products = Product.objects.filter(
            id__in=product_ids
        )

        products_map = {
            product.id: product
            for product in products
        }

        cart = copy.deepcopy(self.cart)

        for item in cart.values():
            item['product'] = products_map.get(
                item['product_id']
            )

            item['price'] = Decimal(item['price'])
            item['total_price'] = (
                    item['price'] * item['quantity']
            )

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

