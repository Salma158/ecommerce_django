from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializer import ReviewSerializer
from products.models import Product

@api_view(['POST'])
def create_product_review(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    already_exists = product.review_set.filter(user=user).exists()
    if already_exists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif data.get('rating', 0) == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data.get('comment', ''),
        )

        product.numReviews = product.review_set.count()
        product.rating = product.review_set.aggregate(models.Avg('rating'))['rating__avg']
        product.save()

        return Response('Review Added')
