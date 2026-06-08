from decimal import Decimal, ROUND_HALF_UP

from django.shortcuts import render, redirect

from cart.cart import Cart
from main.models import PromoCode
from orders.forms import CreateOrderForm
from orders.models import OrderItem


def create_order(request):
    cart = Cart(request)
    promo = request.session.get('promo', None)
    promo_obj = None
    subtotal = cart.get_total()
    if promo:
        promo_obj = PromoCode.objects.filter(name=promo).first()
    total = cart.get_total(promo=promo_obj)
    if request.method == "POST":
        form = CreateOrderForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                price = item['price']
                if promo_obj:
                    discount_amount = item['price'] * Decimal(promo_obj.discount) / Decimal("100")
                    price = (item['price'] - discount_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                OrderItem.objects.create(
                    product=item['product'],
                    price=price,
                    quantity=item['quantity'],
                    order=order
                )
            cart.clear_items()
            request.session['order_id'] = order.id
            return redirect('main:home')
    else:
        form = CreateOrderForm(request=request)
        return render(request, 'orders/create_order.html', {'form': form, 'cart': cart, 'subtotal': subtotal, 'total':total, 'promo': promo_obj, 'discount_dollar': (subtotal - total)})