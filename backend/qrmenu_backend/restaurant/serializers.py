from rest_framework import serializers
from .models import Restaurant, Category, MenuItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    restaurant = serializers.StringRelatedField()  # Show restaurant name
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    class Meta:
        model = MenuItem
        fields = '__all__'
