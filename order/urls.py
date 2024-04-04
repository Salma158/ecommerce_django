from django.urls import path
from .views import getAllOrders, getOrderById

urlpatterns =[
    path('',getAllOrders,name='getAllOrders'),
    path('<str:pk>',getOrderById,name='getOrderById'),
]
