from django import forms

from orders.models import Order


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request and self.request.user.is_authenticated:
            self.initial['first_name'] = self.request.user.first_name
            self.initial['last_name'] = self.request.user.last_name
            self.initial['email'] = self.request.user.email
            self.initial['phone'] = self.request.user.phone

    def save(self, commit = True):
        order = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            order.user = self.request.user
        if commit:
            order.save()
        return order

