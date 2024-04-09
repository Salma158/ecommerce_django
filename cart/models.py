from django.db import models
from users.models import Account
from products.models import Product
from django.core.validators import MinValueValidator


class Cart(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE , related_name='cart')
    #product = models.ManyToManyField(Product, related_name='carts', through='CartItem')


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)],default=1)
