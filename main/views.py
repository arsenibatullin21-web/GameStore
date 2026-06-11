from os import name

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from main.forms import ProductAddForm
from main.models import Product, News, Genre, Platform


class HomePageView(ListView):
    model = Product
    template_name = 'main/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['free_games'] = Product.objects.filter(price=0)
        return context

class NewsPageView(ListView):
    model = News
    template_name = 'main/news.html'

class CatalogPageView(ListView):
    model = Product
    template_name = 'main/catalog.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_template_names(self):
        if self.request.headers.get('HX-Request') == 'true':
            target = self.request.headers.get('HX-Target')
            if target == 'catalog-shell':
                return ['partial/catalog_partial.html']
            return ['main/catalog.html']
        return ['main/catalog.html']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['platforms'] = Platform.objects.all()
        context['selected_page'] = self.request.GET.get('page', None)
        context['selected_price'] = self.request.GET.get('price', None)
        context['selected_genre'] = self.request.GET.getlist('genre', None)
        context['selected_platform'] = self.request.GET.getlist('platform', None)
        context['selected_sort'] = self.request.GET.get('sort', None)
        context['selected_search'] = self.request.GET.get('q', None)

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = query_params.urlencode()
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        price_filter = self.request.GET.get('price', None)
        genre = self.request.GET.getlist('genre', None)
        platform = self.request.GET.getlist('platform', None)
        sort = self.request.GET.get('sort', None)
        search = self.request.GET.get('q', None)


        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(genre__name__icontains=search))
        if sort:
            if sort == 'New':
                queryset = queryset.order_by('-created_at')
            elif sort == 'Recent_upd':
                queryset = queryset.order_by('-updated_at')
            elif sort == 'Lth':
                queryset = queryset.order_by('price')
            elif sort == 'Htl':
                queryset = queryset.order_by('-price')
            elif sort == 'Discount':
                queryset = queryset.order_by('-discount')

        if genre:
            queryset = queryset.filter(genre__slug__in=genre)
        if platform:
            queryset = queryset.filter(platform__slug__in=platform)
        if price_filter:
            if price_filter == 'free':
                queryset = queryset.filter(price=0)
            elif price_filter == 'under-10':
                queryset = queryset.filter(price__lte=10)
            elif price_filter == 'below-10':
                queryset = queryset.filter(price__gte=10)
            elif price_filter == 'discounted':
                queryset = queryset.filter(discount__gt=0)

        return queryset
        


class ProductAddView(CreateView):
    model = Product
    template_name = 'main/product_add.html'
    form_class = ProductAddForm
    success_url = reverse_lazy('main:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['platforms'] = Platform.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'product_slug'

    def get_template_names(self):
        if self.request.headers.get('HX-Request') == 'true':
            return ['partial/cart-budge.html']
        return ['main/product_detail.html']