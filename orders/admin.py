from django.contrib import admin
from django.utils.safestring import mark_safe

from orders.models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 2

def order_stripe_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f"<a href='{url}' target='_blank'>{obj.stripe_id}</a>"
        return mark_safe(html)
    return ''

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'phone', 'paid', 'payment_status', order_stripe_payment]
    inlines = [OrderItemInline]