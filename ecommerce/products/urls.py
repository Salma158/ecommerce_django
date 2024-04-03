# from products import views
# from django.urls import path
# urlpatterns = [
#     path('',views.getRoutes,name="Routes"),
#     path('products/',views.getProducts , name='getProducts'),
#     path('categories/',views.getCategories , name='getCategories')

# ]



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




# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.getRoutes, name="Routes"),
#     path('products/', views.getProducts, name='getProducts'),
#     path('products/<int:pk>/', views.getProductDetail, name='getProductDetail'),
#     path('products/<int:pk>/update/', views.updateProductDetail, name='updateProductDetail'),  # Added for updating product
#     path('products/<int:pk>/delete/', views.deleteProduct, name='deleteProduct'),  # Added for deleting product
#     path('categories/', views.getCategories, name='getCategories'),
#     path('categories/<int:pk>/', views.getCategoryDetail, name='getCategoryDetail'),
#     path('categories/<int:pk>/update/', views.updateCategoryDetail, name='updateCategoryDetail'),  # Added for updating category
#     path('categories/<int:pk>/delete/', views.deleteCategory, name='deleteCategory'),  # Added for deleting category
#     path('categories/<int:category_pk>/products/', views.getProductsByCategory, name='getProductsByCategory'),
#     path('products/search/<str:query>/', views.productSearch, name='productSearch'),
#     path('upload_image/', views.upload_image, name='upload_image'),  # Added for image upload
# ]
