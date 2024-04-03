from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Registeration.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profiles/', views.UserProfileDetailAPIView.as_view(), name='profile-detail'),

]
