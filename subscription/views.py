import stripe
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.timezone import now

from GameStore import settings
from subscription.models import Subscription
from user.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


def subscription_view(request):
    basic = stripe.Product.retrieve('prod_Ug3oWU7cU3527S')
    pro = stripe.Product.retrieve('prod_Ug3oGtqgGzom2j')
    premium = stripe.Product.retrieve('prod_Ug3pifkG1p6wZH')

    price_basic = stripe.Price.list(
        product=basic.id,
        active=True
    )
    price_pro = stripe.Price.list(
        product=pro.id,
        active=True
    )
    price_premium = stripe.Price.list(
        product=premium.id,
        active=True
    )

    subscriptions = {
        'basic': {
            'product': basic,
            'price': price_basic.data[0],
        },
        'pro': {
            'product': pro,
            'price': price_pro.data[0],
        },
        'premium': {
            'product': premium,
            'price': price_premium.data[0],
        }
    }


    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('user:login')}?next={request.get_full_path()}")
        price_id = request.POST.get('price_id')
        subscription = Subscription.objects.filter(user=request.user).first()


        if subscription:
            stripe_subscription = stripe.Subscription.retrieve(subscription.subscription_id)
            item = stripe_subscription['items']['data'][0]
            stripe.Subscription.modify(
                subscription.subscription_id,
                items = [{
                    'id': item['id'],
                    'price': price_id
                }],
                cancel_at_period_end = False
            )
            price = stripe.Price.retrieve(price_id)
            product = stripe.Product.retrieve(price['product'])

            subscription.start_date = now()
            subscription.product_name = product.name
            subscription.price = price['unit_amount'] / 100
            subscription.end_date = None
            subscription.canceled_at = None
            subscription.save()
            return redirect('subscription:profile')
        else:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1
                     }
                ],
                payment_method_types=['card',],
                mode='subscription',
                success_url = request.build_absolute_uri(reverse("subscription:create")) + f"?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url = request.build_absolute_uri(f'{reverse("subscription:subscription")}'),
                metadata={
                    'user_id': request.user.id,
                }
            )
            return redirect(checkout_session.url, code=303)
    return render(request, 'subscription/subscription.html', {'subscriptions': subscriptions})


def create_subscription(request):
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    subscription = stripe.Subscription.retrieve(session.subscription)
    price = subscription['items']['data'][0]['price']
    product_id = price['product']
    product = stripe.Product.retrieve(product_id)

    if checkout_session_id:
        Subscription.objects.create(
            user=request.user,
            customer_id=session.customer,
            subscription_id=session.subscription,
            product_name=product.name,
            price=price['unit_amount'] / 100,
            interval=price['recurring']['interval'],
            start_date=datetime.fromtimestamp(subscription['start_date']),
        )
    return redirect('subscription:profile')

def my_sub(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    subscription = Subscription.objects.filter(user=request.user).first()
    return render(request, 'subscription/my_sub.html', {'subscription': subscription})

def cancel_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, user=request.user, subscription_id=subscription_id)
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True
    )
    subscription.canceled_at = now()
    stripe_subscription = stripe.Subscription.retrieve(subscription_id)
    subscription.end_date = datetime.fromtimestamp(stripe_subscription.canceled_at)
    subscription.save()
    return redirect('subscription:profile')