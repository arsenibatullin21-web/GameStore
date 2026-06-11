from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from main.models import Product, PromoCode


# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    promo = request.session.get('promo', None)
    promo_obj = None
    if promo:
        promo_obj = PromoCode.objects.filter(name__iexact=promo).first()

    if request.headers.get('HX-Request') == 'true':
        target = request.headers.get('HX-Target') == 'true'
        if target == 'messages':
            return render(request, 'partial/messages.html', {'cart': cart,'subtotal': cart.get_total(),'total': cart.get_total(promo=promo_obj), 'promo': promo})
        return render(request, 'partial/cart-response.html', {'cart': cart,'subtotal': cart.get_total(),'total': cart.get_total(promo=promo_obj), 'promo': promo})
    return render(request, 'cart/cart_detail.html', {'cart': cart,'subtotal': cart.get_total(),'total': cart.get_total(promo=promo_obj), 'promo': promo})

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

def apply_promo(request):
    promo_name = request.GET.get('promocode', '')
    promo = PromoCode.objects.filter(name=promo_name).first()

    if promo:
        request.session['promo'] = promo_name
        messages.success(request, "Promo code applied successfully")
    else:
        messages.error(request, 'Promo code in invalid')

    return redirect('cart:detail')

def remove_promo(request):
    request.session.pop('promo', None)
    request.session.modified = True
    messages.info(request, 'Promo code was removed')
    return redirect('cart:detail')
