
from django.contrib import admin
from django.urls import path, include

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('news/', views.NewsPageView.as_view(), name='news'),
    path('browse/', views.CatalogPageView.as_view(), name='catalog'),
    path('product/add/', views.ProductAddView.as_view() ,name='product_add')
]
