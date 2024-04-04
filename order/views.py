from django.shortcuts import get_object_or_404, render
# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Order
from .serializers import  OrderSerializer,OrderItemsSerializer
from django.utils import timezone


@api_view(['GET','POST'])
def getAllOrders(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method =='POST':
        serializer = OrderSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PATCH':
        pass
    elif request.method == 'DELETE':
        pass

@api_view(['GET','PATCH','DELETE'])
def getOrderById(request, pk):
    try:
        order = Order.objects.get(order_id=pk)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    
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
    elif order.order_status == 'Cancelled' or order.shipping_status == 'Cancelled':
        order.shipping_status = data.get("shipping_status", "Cancelled")
        order.order_status = data.get("order_status", "Cancelled")
        order.save()
