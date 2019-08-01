from django.db import models
from django.conf import settings
from django.shortcuts import reverse

class Items(models.Model):
    title = models.CharField(max_length = 255, blank=True)
    price = models.FloatField(blank=True)
    discount_price = models.FloatField(blank=True, default= 0)
    name = models.CharField(max_length = 255, blank=True)
    tag = models.CharField(max_length = 30, blank=True)
    image =models.FileField(upload_to= 'images/', blank = True)
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:product', kwargs={'pk': self.id})

    def add_to_cart(self):
        return reverse('core:add-to-cart', kwargs={'pk': self.id})
        
    def remove_from_cart(self):
        return reverse('core:remove-from-cart', kwargs={'pk': self.id})


class OrderItem(models.Model):
    item = models.ForeignKey(Items, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)


    def __str__(self):
        return self.item.title
    
    def get_item_total_price(self):
        return self.quantity * self.item.price
    
    def get_discount_price(self):
        return self.quantity * self.item.discount_price
    
    def get_save_amount(self):
        return self.get_item_total_price() - self.get_discount_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_price()
        else:
            return self.get_item_total_price()

    
        
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, null=True) 
    address =models.CharField(max_length = 255)
    zip = models.CharField(max_length = 30)
    country =models.CharField(max_length = 30)
    email = models.CharField(max_length = 50)
    payment_method = models.CharField(max_length = 10)
    default_address = models.BooleanField(default= False)


    def __str__(self):
        return self.address


class Order(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = True)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, null = True)


    def __str__(self):
        return self.user.username

    def get_final_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


