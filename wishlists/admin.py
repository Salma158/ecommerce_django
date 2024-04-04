from .models import Wishlist
from django.contrib import admin

class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_list')

    def product_list(self, obj):
        return ", ".join([p.productname for p in obj.products.all()])

admin.site.register(Wishlist, WishListAdmin)