from rest_framework import serializers
from rest_framework import serializers
from .models import Order, OrderItems
from products.serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItems
        fields = '__all__'
