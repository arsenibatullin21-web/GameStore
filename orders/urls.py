from django.urls import path, include

from orders import views
app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create')
]