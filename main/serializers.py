from django.utils.html import escape

from pycparser.c_ast import Return
from rest_framework import serializers
from main.models import Product, Genre
class ProductSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True, many=False)
    class Meta:
        model = Product
        fields ='__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError('Length of the name is too long!')
        return escape(value.strip())

class CreateProductSerializer(ProductSerializer):
    pass

class UpdateProductSerializer(ProductSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

class GenreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Genre
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        genre = Genre.objects.create(**validated_data)
        for product in products:
            Product.objects.create(genre=genre, **product)

        return genre

