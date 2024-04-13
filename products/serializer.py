
from rest_framework import serializers
from .models import Product, Category
from RatingReview.models import Review
# from RatingReview.serializer import ReviewSerializer
from .models import ProductImage

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')

class ProductSerializer(serializers.ModelSerializer):
    productcategory = CategorySerializer()
    num_reviews = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)  

    class Meta:
        model = Product
        fields = '__all__'


    def get_num_reviews(self, obj):       
        from RatingReview.models import Review
        return Review.objects.filter(product=obj).count()

  
