from django.urls import path
from .views import RestaurantListView, CategoryListView, MenuItemListView

urlpatterns = [
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('menu-items/', MenuItemListView.as_view(), name='menu-item-list'),
]
