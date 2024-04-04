from django.urls import path
from .views import WishlistGetandAdd, WishlistDelete

urlpatterns = [
    path('', WishlistGetandAdd.as_view(), name='wishlist'),
    path('<int:product_id>/', WishlistDelete.as_view(), name='wishlist-delete'),
]
