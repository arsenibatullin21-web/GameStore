from random import choices

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Platform(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category', blank=True, default='profile_images/noimgage.jpg')
    description = models.TextField()

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    objects = None
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    description = models.TextField(blank=True, null=True)
    short_description = models.TextField()

    price = models.DecimalField(decimal_places=2,max_digits=10, default=0)
    discount = models.IntegerField(default=0)

    cover_image = models.ImageField(upload_to='products/main/%Y/%m/%d', default='profile_images/noimgage.jpg')
    trailer_url = models.URLField(blank=True)

    genre = models.ForeignKey(to='Genre', on_delete=models.CASCADE, related_name='products')
    platform = models.ForeignKey(to='Platform', on_delete=models.CASCADE, related_name='products')

    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'product_slug': self.slug})

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d')
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.product.name} - {self.image.name}'


class News(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    short_description = models.TextField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='news/%Y/%m/%d',  default='profile_images/noimgage.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

