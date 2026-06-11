from django.urls import path

from payment import views, webhooks

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('success/', views.payment_success, name='success'),
    path('webhook/', webhooks.payment_webhook ,name='webhook')
]