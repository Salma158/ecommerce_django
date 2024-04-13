
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializer import ReviewSerializer
from products.models import Product
from django.db.models import Avg  
from users.models import Account

@api_view(['POST'])
def create_product_review(request, pk):
    try:
        product = Product.objects.get(_id=pk)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data


    if data.get('rating', 0) == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        review = Review.objects.create(
            user = request.user,
            product=product,
            name=data.get('name', ''),  
            rating=data['rating'],
            comment=data.get('comment', ''),
        )

        
        total_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']       
        product.rating = total_rating
        
        product.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_product_reviews(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        total_reviews = reviews.count()  
        data = serializer.data
        for review in data:
            review['num_reviews'] = total_reviews
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)