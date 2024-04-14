from django.urls import path
from . import views


urlpatterns = [
    # General routes
    path('', views.getRoutes, name="Routes"),
    
    # Product routes
    path('products/', views.getProducts, name='getProducts'),
    path('products/<int:pk>/', views.getProduct, name='getProduct'),
    path('products/<int:pk>/update/', views.updateProduct, name='updateProduct'),
    path('products/<int:pk>/delete/', views.deleteProduct, name='deleteProduct'),
    path('products/search/<str:query>/', views.product_search, name='product_search'),

    
    # Category routes
    path('categories/', views.getCategories, name='getCategories'),
    path('categories/create/', views.createCategory, name='createCategory'),
    path('categories/<int:pk>/', views.getCategory, name='getCategory'),
    path('categories/<int:pk>/update/', views.updateCategory, name='updateCategory'),
    path('categories/<int:pk>/delete/', views.deleteCategory, name='deleteCategory'),
    path('categories/<int:category_pk>/products/', views.getProductsByCategory, name='getProductsByCategory'),
    
    # Other routes
    path('upload-image/', views.upload_image, name='upload_image'),
    path('products/top/', views.getTopProducts, name='top-products'),

    path('products/sorted-by-price/', views.getProductsByPrice, name='getProductsSortedByPrice'),


]