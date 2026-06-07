from django.contrib import admin
from django.urls import path, include

from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<str:product_id>', views.cart_add, name='add'),
    path('remove/<str:product_id>', views.cart_remove, name='remove'),
    path('clear/', views.cart_clear, name='clear'),
    path('upd_quantity/<str:product_id>', views.cart_upd_quantity, name='update'),
]