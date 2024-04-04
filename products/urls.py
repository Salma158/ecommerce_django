from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="Routes"),
    path('products/', views.getProducts, name='getProducts'),
    path('products/<int:pk>/', views.getProductDetail, name='getProductDetail'),
    path('categories/', views.getCategories, name='getCategories'),
    path('categories/<int:pk>/', views.getCategoryDetail, name='getCategoryDetail'),
    path('categories/<int:category_pk>/products/', views.getProductsByCategory, name='getProductsByCategory'),
    path('products/search/<str:query>/', views.productSearch, name='productSearch'),
    path('upload-image/', views.upload_image, name='upload_image'),

]

