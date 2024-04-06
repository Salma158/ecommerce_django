# Generated by Django 5.0.3 on 2024-04-06 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_product_options_remove_product_numreviews"),
    ]

    operations = [
        migrations.AlterModelOptions(name="product", options={},),
        migrations.AlterField(
            model_name="product",
            name="productcategory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="products.category",
            ),
        ),
    ]
