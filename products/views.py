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
# from django.shortcuts import render
# # from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# # from .products import products
# from .models import Product
# from .models import Category
# from .serializer import ProductSerializer
# from .serializer import CategorySerializer
# from rest_framework.permissions import IsAuthenticated
# @api_view(['GET'])
# def getRoutes(requests):
#     return Response('Hello')

# @api_view(['GET'])
# # @permission_class([IsAuthenticated])
# def getProducts(requests):
#     products=Product.objects.all()
#     serializer = ProductSerializer(products,many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getCategories(requests):
#     categories=Category.objects.all()
#     serializer = CategorySerializer(categories,many=True)
#     return Response(serializer.data)





# from rest_framework import status
# from django.core.files.storage import FileSystemStorage

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Product, Category
# from .serializer import ProductSerializer
# from .serializer import CategorySerializer
# @api_view(['GET'])
# def getRoutes(request):
#     return Response('Hello')

# @api_view(['GET'])
# def getProducts(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getCategories(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getCategoryDetail(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = CategorySerializer(category)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getProductDetail(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getProductsByCategory(request, category_pk):
#     products = Product.objects.filter(productcategory=category_pk)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def productSearch(request, query):
#     products = Product.objects.filter(productname__icontains=query)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# def upload_image(request):
#     if request.method == 'POST' and request.FILES['image']:
#         image_file = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(image_file.name, image_file)
#         uploaded_file_url = fs.url(filename)
#         return JsonResponse({'uploaded_file_url': uploaded_file_url})
#     return HttpResponseBadRequest()



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage

from .models import Product, Category
from .serializer import ProductSerializer, CategorySerializer

@api_view(['GET'])
def getRoutes(request):
    return Response('Hello')

@api_view(['GET', 'POST'])
def getProducts(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def getProductDetail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def getCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def getCategoryDetail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getProductsByCategory(request, category_pk):
    products = Product.objects.filter(productcategory=category_pk)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def productSearch(request, query):
    products = Product.objects.filter(productname__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# def upload_image(request):
#     if request.method == 'POST' and request.FILES['image']:
#         image_file = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(image_file.name, image_file)
#         uploaded_file_url = fs.url(filename)
#         return JsonResponse({'uploaded_file_url': uploaded_file_url})
#     return HttpResponseBadRequest()

from cloudinary.uploader import upload


@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        # Upload image to Cloudinary
        uploaded_file = upload(image_file)
        return JsonResponse({'uploaded_file_url': uploaded_file['secure_url']})
    return HttpResponseBadRequest()

