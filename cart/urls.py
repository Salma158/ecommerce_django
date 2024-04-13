from django.urls import path
from .views import CartList, CartItemDelete, CartItemUpdate

urlpatterns =[
    path('',CartList.as_view(), name='add_to_cart'),
    path('',CartList.as_view(), name='cart_list'),
    path('<str:pk>/delete',CartItemDelete.as_view(), name='remove_from_cart'),
    path('<str:pk>/update',CartItemUpdate.as_view(), name='cart_list')

]
