from django.db import models
from products.models import Product
from users.models import Account

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name)
