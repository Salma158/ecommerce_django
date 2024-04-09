from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, serializers
from .models import Cart, CartItems
from .serializers import CartItemsSerializer
from rest_framework.generics import ListCreateAPIView, DestroyAPIView,UpdateAPIView
from products.models import Product


class CartList(ListCreateAPIView):
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItems.objects.filter(cart__user=user)
    
    def post(self, request):
        user = request.user
        _id = request.data.get('product')
        #quantity = request.data.get('quantity')
        cart, created = Cart.objects.get_or_create(user=user)
        product = Product.objects.get(pk= _id)
        cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemDelete(DestroyAPIView):
    queryset = CartItems.objects.all()
    permission_classes = [IsAuthenticated]   
    def delete(self,request, pk):
        user = request.user
        cart_item = get_object_or_404(CartItems, cart__user=user, product=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemUpdate(UpdateAPIView):
    serializer_class = CartItemsSerializer
    queryset = CartItems.objects.all()
    permission_classes = [IsAuthenticated]  
    def patch(self, request, pk):
        user = request.user
        action = request.data.get('action')
        cart_item = get_object_or_404(CartItems, cart__user=user, product=pk)
        if action not in ('Increase', 'Decrease'):
            raise serializers.ValidationError({'error': "Action can only be 'INCREASE' or 'DECREASE'"})
        if action == "Increase":
            product = cart_item.product
            if product.stock > cart_item.quantity:
                cart_item.quantity += 1
            else:
                raise serializers.ValidationError({'error': 'No more available quantity'})
        elif action == "Decrease":
            if cart_item.quantity > 1:
                cart_item.quantity-=1
            else:
                cart_item.delete()
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)


   
