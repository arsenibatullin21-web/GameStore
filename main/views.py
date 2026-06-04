from django.shortcuts import render
from django.views.generic import ListView

from main.models import Product


class HomePageView(ListView):
    model = Product
    template_name = 'main/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['free_games'] = Product.objects.filter(price=0)
        return context

