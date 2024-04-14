from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import AccountSerializer, AuthSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from cloudinary.uploader import upload
from rest_framework.decorators import api_view
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .serializers import ForgotPasswordSerializer
from .models import Account
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ResetPasswordSerializer
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password




class Registeration(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = {
                "message": "User created Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        uploaded_file = upload(image_file)
        return JsonResponse({'uploaded_file_url': uploaded_file['secure_url']})
    return HttpResponseBadRequest()


class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("hiii")
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = Account.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                frontend_reset_url = settings.FRONTEND_URL + '/reset-password?token=' + token + '&uid=' + uid
                send_mail(
                    'Reset your password',
                    f'Hi {user.username},\n\n'
                    f'You requested to reset your password. Please click on the link below to reset your password:\n\n'
                    f'{frontend_reset_url}\n\n'
                    'Thank you.\n',
                    'bloomosbloomos40@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                return Response({'message': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No user found with this email'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            uid = serializer.validated_data.get('uid')

            try:
                user_id = urlsafe_base64_decode(uid)
                user_id = smart_bytes(user_id).decode('utf-8')
                user = Account.objects.get(pk=user_id)
            except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.password = make_password(serializer.validated_data.get('new_password'))
                user.save()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)