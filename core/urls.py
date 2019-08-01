from django.urls import path
from .views import (item_list, product, checkout, add_to_cart,
remove_from_cart, order_summary,add_single_item,remove_single_item, order_done)

app_name = 'core'

urlpatterns = [
    path('', item_list, name = 'item-list'),
    path('product/<int:pk>', product, name = 'product'),
    path('order-summary', order_summary, name = 'order-summary'),
    path('add-to-cart/<int:pk>', add_to_cart, name = 'add-to-cart'),
    path('add-single-item/<int:pk>', add_single_item, name = 'add-single-item'),
    path('remove-single-item/<int:pk>', remove_single_item, name = 'remove-single-item'),
    path('remove-from-cart/<int:pk>', remove_from_cart, name = 'remove-from-cart'),
    path('order-done/<int:pk>', order_done, name = 'order-done'),
    path('checkout', checkout, name = 'checkout')
]