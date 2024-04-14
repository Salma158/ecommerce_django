from django.shortcuts import get_object_or_404, render
# from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Order,OrderItems
from .serializers import  OrderSerializer, OrderItemsSerializer
from cart.models import CartItems
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

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.product.productname,
            },
            'unit_amount': int(item.product.price * 100),
        },
        'quantity': item.quantity,
    } for item in cart_items]

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=user, total_price=total_price)
    for item in cart_items:
        OrderItems.objects.create(
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            order_id=order
        )
        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=settings.SITE_URL + f'?success=true&session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=settings.SITE_URL + '?canceled=true',
        )
        print("Checkout Session ID:", checkout_session.id)
        return Response({'checkout_url': checkout_session.url})
    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllOrders(request):
    user = request.user
    if request.method == 'GET':
        
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
    # elif request.method =='POST':
    #     serializer = OrderSerializer(data = request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)




        

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    try:
        order = Order.objects.prefetch_related('orderitems_set').get(order_id=pk)
        serializer = OrderSerializer(order)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
    if order.user != request.user:
        return Response({"detail": "You do not have permission to access this order."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        order_serializer = OrderSerializer(order)
        order_items_serializer = OrderItemsSerializer(order.orderitems_set.all(), many=True)
        data = {
            "order": order_serializer.data,
            "order_items": order_items_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        order.delete()
        return Response({"detail": f"Order with ID {pk} is deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PATCH':
        if order.order_status != 'Cancelled' and order.shipping_status != 'Delivered':
            updateOrderById(order, request.data)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Cannot update order. It is already cancelled or delivered."}, status=status.HTTP_400_BAD_REQUEST)


def updateOrderById(order, data):
    if order.order_status != 'Cancelled' and order.shipping_status != 'Delivered':
        order.order_status = data.get("order_status", order.order_status)
        order.shipping_status = data.get("shipping_status", "Cancelled")
        order.delivery_date = data.get("delivery_date", order.delivery_date)
        order.save()
    if order.order_status == 'Cancelled' or order.shipping_status == 'Cancelled':
        order.shipping_status = data.get("shipping_status", "Cancelled")
        order.order_status = data.get("order_status", "Cancelled")
        for order_item in order.orderitems_set.all():
                        order_item.product.stock += order_item.quantity
                        order_item.product.save()
        order.save()
    
