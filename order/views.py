from django.shortcuts import get_object_or_404, render
# from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Order,OrderItems
from .serializers import  OrderSerializer
from datetime import datetime, timedelta
from django.utils import timezone
from cart.models import CartItems
from django.shortcuts import redirect
import stripe
from django.conf import settings
from django.db import transaction

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkoutView(request):
    user = request.user
    cart_items = CartItems.objects.filter(cart__user=user)
    if not cart_items:
        return Response({"error": "The Cart Is Empty"}, status=status.HTTP_400_BAD_REQUEST)
    line_items = []

    for cart_item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': cart_item.product.productname,
                },
                'unit_amount': int(cart_item.product.price * 100),  # Price in cents
            },
            'quantity': cart_item.quantity,
        })

    try:
        with transaction.atomic():
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=settings.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            order = None
            
            # Your code to place the order after confirming the payment
            if checkout_session.payment_status == 'paid':
                total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
                order_instance = Order.objects.create(
                    user=user,
                    total_price=total_price,
                )

                for cart_item in cart_items:
                    OrderItems.objects.create(
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price,
                        order_id=order_instance.id  # Ensure to use order_instance.id instead of order_instance
                    )

                # Delete cart items after order creation
                cart_items.delete()

                # Placeholder for the order
                order = order_instance

            return Response({'url': checkout_session.url, 'order_id': order.id if order else None}, status=status.HTTP_201_CREATED)
    except stripe.error.StripeError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllOrders(request):
    user = request.user
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # elif request.method =='POST':
    #     serializer = OrderSerializer(data = request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)




        

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    try:
        order = Order.objects.get(order_id=pk)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)\
        
    if order.user != request.user:
        return Response({"detail": "You do not have permission to access this order."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        order.delete()
        return Response({"detail": f"Order with ID {pk} is deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PATCH':
        updateOrderById(order, request.data)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

def updateOrderById(order, data):
    if order.order_status != 'Cancelled' and order.shipping_status != 'Delivered':
        order.order_status = data.get("order_status", order.order_status)
        order.shipping_status = data.get("shipping_status", order.shipping_status)
        order.delivery_date = data.get("delivery_date", order.delivery_date)
        order.save()
    if order.order_status == 'Cancelled' or order.shipping_status == 'Cancelled':
        order.shipping_status = data.get("shipping_status", "Cancelled")
        order.order_status = data.get("order_status", "Cancelled")
        order.save()
    
