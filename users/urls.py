from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Registeration.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profiles/', views.UserProfileDetailAPIView.as_view(), name='profile-detail'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('forgetpassword/', views.PasswordResetAPIView.as_view(), name='password_reset'),
    path('resetpassword/', views.ResetPasswordAPIView.as_view(), name='reset-password'),

]
