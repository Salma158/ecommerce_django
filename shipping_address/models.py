from django.db import models
from django.contrib.auth.models import User
from order.models import Order

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.AutoField(primary_key = True, editable = False)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=60)
    postalCode = models.CharField(max_length=10)
    country = models.CharField(max_length=60)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.address)