# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Review
# from .serializer import ReviewSerializer
# from products.models import Product

# @api_view(['POST'])
# def create_product_review(request, pk):
#     user = request.user
#     product = Product.objects.get(_id=pk)
#     data = request.data

#     already_exists = product.review_set.filter(user=user).exists()
#     if already_exists:
#         content = {'detail': 'Product already reviewed'}
#         return Response(content, status=status.HTTP_400_BAD_REQUEST)

#     elif data.get('rating', 0) == 0:
#         content = {'detail': 'Please select a rating'}
#         return Response(content, status=status.HTTP_400_BAD_REQUEST)

#     else:
#         review = Review.objects.create(
#             user=user,
#             product=product,
#             name=user.first_name,
#             rating=data['rating'],
#             comment=data.get('comment', ''),
#         )

#         product.numReviews = product.review_set.count()
#         product.rating = product.review_set.aggregate(models.Avg('rating'))['rating__avg']
#         product.save()

#         return Response('Review Added')
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializer import ReviewSerializer
from products.models import Product
from django.db.models import Avg  # Import Avg for aggregation
from users.models import Account

@api_view(['POST'])
def create_product_review(request, pk):
    try:
        product = Product.objects.get(_id=pk)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    # Create a default user or use a placeholder user if no user_id is provided
    default_user = Account.objects.get_or_create(username='anonymous')[0]

    if data.get('rating', 0) == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
        review = Review.objects.create(
            user=default_user,
            product=product,
            name=data.get('name', ''),  # Assuming 'name' can be provided in request data
            rating=data['rating'],
            comment=data.get('comment', ''),
        )

        product.numReviews = product.reviews.count()
        product.rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
        product.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
