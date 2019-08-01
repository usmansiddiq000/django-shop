from django.contrib import admin
from .models import Items, Order, OrderItem, Address

admin.site.register(Items)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)

# Register your models here.
