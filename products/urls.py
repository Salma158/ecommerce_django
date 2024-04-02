from products import views
from django.urls import path
urlpatterns = [
    path('',views.getRoutes,name="Routes"),
    path('products/',views.getProducts , name='getProducts'),
    path('categories/',views.getCategories , name='getCategories')

]