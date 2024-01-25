from products.models import Product,Category,Brand,Color,CartItem,Order
from rest_framework import serializers
from accounts.models import CustomUser
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model =CustomUser
        fields=['id','email','first_name','last_name','user_type']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class BrandSerializer(serializers.ModelSerializer):
    category=serializers.CharField()
    class Meta:
        model=Brand
        fields='__all__'

class ColorSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=Color
        fields=['color']

class ProductSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Product
        fields ='__all__'

class CartSerailizer(serializers.ModelSerializer):

    class Meta:
        model= CartItem
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

