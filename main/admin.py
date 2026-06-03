from django.contrib import admin

from main.models import Product, Platform, Genre, ProductImage


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount', 'is_available']
    list_editable = ['price']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Genre)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}





