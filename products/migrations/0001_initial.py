# Generated by Django 5.0.3 on 2024-04-11 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("categoryname", models.CharField(max_length=30)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("productname", models.CharField(max_length=150)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "productbrand",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("productinfo", models.TextField(blank=True, null=True)),
                (
                    "rating",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("stock", models.IntegerField(blank=True, default=0, null=True)),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                (
                    "_id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                ("numReviews", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "productcategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="products.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="product_images/")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
