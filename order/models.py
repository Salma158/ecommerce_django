from django.db import models
from users.models import Account
from products.models import Product
from shipping_address.models import ShippingAddress
from datetime import timedelta

SHIPPING_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

ORDER_STATUS_CHOICES = (
    ('placed', 'Placed'),
    ('cancelled', 'Cancelled'),
)


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_id = models.AutoField(primary_key=True, editable=False)
    delivery_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    placing_date = models.DateTimeField(auto_now_add=True)
    shipping_status = models.CharField(max_length=20, choices=SHIPPING_STATUS_CHOICES, default='pending')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='placed')
    total_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"Order ID: {self.order_id}, Total Price: {self.total_price}"
    
    def calculate_delivery_date(self):
        if self.placing_date:
            return self.placing_date + timedelta(days=5)
        return None

    @property
    def estimated_delivery_date(self):
        return self.calculate_delivery_date()

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = self.calculate_delivery_date()
        super().save(*args, **kwargs)
    
class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f"Product: {self.product}, Quantity: {self.quantity}"
