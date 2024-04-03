from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Wishlist
from .serializers import WishlistSerializer
from products.models import Product
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


class WishlistPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WishlistGetandAdd(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer
    pagination_class = WishlistPagination

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        product_id = request.data.get('product')
        product = serializer.validated_data['product']
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        product = get_object_or_404(Product, pk=product_id)
        wishlist.product.add(product)
        
        if created:
            return Response({"message": "Wishlist created and product added successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Product added to wishlist successfully."}, status=status.HTTP_201_CREATED)

class WishlistDelete(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def delete(self, request, product_id):
        user = request.user
        wishlist = get_object_or_404(Wishlist, user=user)
        product = get_object_or_404(Product, pk=product_id)
        
        if product in wishlist.product.all():
            wishlist.product.remove(product)
            return Response({"message": "Product removed from wishlist successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)

