from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import ShippingAddress
from rest_framework.response import Response
from .serializers import  ShippingAddressSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ShippingAddress, userAdresses


# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated]) 
def addressList(request):
    if request.method == 'GET':
        addresses = ShippingAddress.objects.all()
        serializer = ShippingAddressSerializer(addresses, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method =='POST':
        serializer = ShippingAddressSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        shipping_address = serializer.save()
        user = request.user
        user_address = userAdresses.objects.create(shipping_address=shipping_address, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    