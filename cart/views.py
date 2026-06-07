from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from main.models import Product


# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    print(list(cart))
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'total': cart.get_total()})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect(product.get_absolute_url())

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart:detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear_items()
    return redirect('cart:detail')


def cart_upd_quantity(request, product_id):
    cart = Cart(request)
    action = request.GET.get('action', '')
    cart.update_quantity(product_id=product_id, action=action)
    return redirect('cart:detail')