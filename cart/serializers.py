from rest_framework import serializers
from .models import Cart, CartItems
from products.serializer import ProductSerializer

class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItems
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemsSerializer()
    class Meta:
        model = Cart
        fields = '__all__'