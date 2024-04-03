from rest_framework import serializers
from products.models import Product

class WishlistSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def validate_product(self, value):
        if not Product.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value