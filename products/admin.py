from django.contrib import admin
from .models import Product
from .models import Category
from .models import ProductImage
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)