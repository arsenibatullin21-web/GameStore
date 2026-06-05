from django import forms

from main.models import Product


class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'slug','description', 'short_description', 'price','discount','platform', 'cover_image', 'trailer_url', 'genre', 'stock', 'is_available', 'is_featured']
