from django.db import models
from users.models import Account
from products.models import Product
from django.core.validators import MinValueValidator


class Cart(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE , related_name='cart')


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)],default=1)

    def __str__(self):
        return f"{self.product.productname} {self.quantity} {self.product.stock} {self.product.image}"
