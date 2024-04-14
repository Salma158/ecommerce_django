from django.urls import path
from .views import getAllOrders, getOrderById, checkoutView

urlpatterns =[
    path('checkout-session',checkoutView, name='checkout'),
    path('',getAllOrders,name='getAllOrders'),
    path('<str:pk>',getOrderById,name='getOrderById'),
    path('<str:pk>/cancel',getOrderById,name='userCancelOrder'),
    
]
