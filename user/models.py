from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='profile_image/', default='profile_images/noimage.jpg')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
