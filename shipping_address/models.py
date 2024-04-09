from django.db import models
from users.models import Account
from django.core.exceptions import ValidationError


def stringValidation(value):
    if not value.isalpha():
        raise ValidationError('Only characters are allowed.')
    
class ShippingAddress(models.Model):
    shipping_address = models.AutoField(primary_key = True, editable = False)
    first_name = models.CharField(max_length=50, validators=[stringValidation], default='prefer not to say')
    last_name = models.CharField(max_length=50, validators=[stringValidation], default='prefer not to say')
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=60, validators=[stringValidation])
    postalCode = models.CharField(max_length=10)
    
    
class userAdresses(models.Model):
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE , related_name='user_addresses')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)