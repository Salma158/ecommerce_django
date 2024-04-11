
from rest_framework import serializers
from .models import Product, Category
from RatingReview.models import Review
# from RatingReview.serializer import ReviewSerializer

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


from .models import ProductImage
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')

class ProductSerializer(serializers.ModelSerializer):
    productcategory = CategorySerializer()
    num_reviews = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)  
    # average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)  

    class Meta:
        model = Product
        fields = '__all__'


    def get_num_reviews(self, obj):
        """
        Returns the number of reviews associated with this product.
        """
        # return obj.reviews.count()
        from RatingReview.models import Review
        return Review.objects.filter(product=obj).count()

    # def get_average_rating(self, obj):
    #     """
    #     Returns the average rating of the product based on its reviews.
    #     """
    #     reviews = obj.reviews.all()
    #     if reviews.exists():
    #         total_rating = sum(review.rating for review in reviews)
    #         return total_rating / reviews.count()
    #     else:
    #         return 0

