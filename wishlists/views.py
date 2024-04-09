from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Wishlist
from .serializers import WishlistSerializer
from products.models import Product
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView



class WishlistGetandAdd(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()

    def get_queryset(self):
        user = self.request.user
        wishlists = Wishlist.objects.filter(user=user)
        return wishlists

    def create(self, request):
        
        product_id = request.data.get('product')
        user = request.user
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        
        try:
            product = Product.objects.get(_id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        if product in wishlist.product.all():
            return Response({"message": "Product already exists in the wishlist."}, status=status.HTTP_400_BAD_REQUEST)

        wishlist.product.add(product)
        
        if created:
            return Response({"message": "Wishlist created and product added successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Product added to wishlist successfully."}, status=status.HTTP_201_CREATED)



class WishlistDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        
        user = request.user
        wishlist = get_object_or_404(Wishlist, user=user)
        product = get_object_or_404(Product, pk=product_id)
        
        if product in wishlist.product.all():  
            wishlist.product.remove(product)
            return Response({"message": "Product removed from wishlist successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)
