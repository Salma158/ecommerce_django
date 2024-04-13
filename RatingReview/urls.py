from django.urls import path
from . import views

urlpatterns = [
    path('products/<int:pk>/reviews/create/', views.create_product_review, name='create_product_review'),
    path('products/<int:pk>/reviews/', views.get_product_reviews, name='product_reviews'),
]
