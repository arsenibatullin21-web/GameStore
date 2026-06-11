from django.urls import path

from subscription import views

app_name = 'subscription'

urlpatterns = [
    path('', views.subscription_view, name='subscription'),
    path('create/', views.create_subscription, name='create'),
    path('my_sub/', views.my_sub,name='profile'),
    path('cancel/<str:subscription_id>', views.cancel_subscription, name='cancel')
]