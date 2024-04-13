from rest_framework import serializers
from .models import Cart, CartItems


class CartItemsSerializer(serializers.ModelSerializer):
    productname = serializers.CharField(source='product.productname')
    stock = serializers.CharField(source='product.stock')
    image = serializers.ImageField(source='product.image')
    _id = serializers.IntegerField(source='product._id')

    class Meta:
        model = CartItems
        fields = ['productname', 'stock', 'image', 'quantity', '_id']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemsSerializer()
    class Meta:
        model = Cart
        fields = '__all__'