# Generated by Django 5.0.3 on 2024-04-11 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("shipping_address", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "order_id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("delivery_date", models.DateTimeField(blank=True, null=True)),
                ("placing_date", models.DateTimeField(auto_now_add=True)),
                (
                    "shipping_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("shipped", "Shipped"),
                            ("delivered", "Delivered"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                (
                    "order_status",
                    models.CharField(
                        choices=[("placed", "Placed"), ("cancelled", "Cancelled")],
                        default="Placed",
                        max_length=20,
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=7, null=True
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "shipping_address",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shipping_address.shippingaddress",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItems",
            fields=[
                ("quantity", models.PositiveIntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
