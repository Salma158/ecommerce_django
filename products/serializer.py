# # from rest_framework import serializers
# # from .models import Product
# # from .models import Category
# # class ProductSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model=Product
# #         fields='__all__'

# # class CategorySerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model=Category
# #         fields='__all__'

# # from rest_framework import serializers
# # from .models import Product, Category

# # class CategorySerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Category
# #         fields = ['categoryname']

# # class ProductSerializer(serializers.ModelSerializer):
# #     # Serialize productcategory field using CategorySerializer
# #     productcategory = CategorySerializer()

# #     class Meta:
# #         model = Product
# #         fields = '__all__'  # Include all fields from the Product model



# from rest_framework import serializers
# from .models import Product, Category

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'categoryname'] 

# class ProductSerializer(serializers.ModelSerializer):
#     productcategory = CategorySerializer()  

#     class Meta:
#         model = Product
#         fields = '__all__'  


from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryname']

class ProductSerializer(serializers.ModelSerializer):
    productcategory = CategorySerializer()  

    class Meta:
        model = Product
        fields = '__all__'
