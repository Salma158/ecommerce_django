from django.urls import path
from .views import getAllOrders, userCancelOrder, getOrderById

urlpatterns =[
    path('',getAllOrders,name='getAllOrders'),
    path('<str:pk>',getOrderById,name='getOrderById'),
    path('<str:pk>/cancel',userCancelOrder,name='userCancelOrder'),
]
