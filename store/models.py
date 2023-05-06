from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url=''
        return url        


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])
    transaction_id = models.CharField(max_length=50, null=True)   
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_item_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
           
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100,null=True) 
    city = models.CharField(max_length=100,null=True) 
    pays = models.CharField(max_length=100,null=True) 
    numtel = models.CharField(max_length=100,null=True) 
    codepostale = models.CharField(max_length=100,null=True)  
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address 