from django.urls import path
from .views import addressList

urlpatterns =[
    path('',addressList,name='address-list'),
]
