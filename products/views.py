from django.shortcuts import render
# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from .products import products
from .models import Product
from .models import Category
from .serializer import ProductSerializer
from .serializer import CategorySerializer
@api_view(['GET'])
def getRoutes(requests):
    return Response('Hello')

@api_view(['GET'])
def getProducts(requests):
    products=Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCategories(requests):
    categories=Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)