from django.urls import path
from .views import (
    RestaurantListCreateView, RestaurantRetrieveUpdateDeleteView,
    CategoryListCreateView, CategoryRetrieveUpdateDeleteView,CategoriesByRestaurantView,
    MenuItemListCreateView, MenuItemRetrieveUpdateDeleteView,MenuItemsByCategoryView,
)

urlpatterns = [
    # Restaurants
    path('restaurants/', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('restaurants/<int:pk>/', RestaurantRetrieveUpdateDeleteView.as_view(), name='restaurant-detail'),

    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('restaurants/<int:restaurant_id>/categories/', CategoriesByRestaurantView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='category-detail'),

    # Menu Items
    path('menu-items/', MenuItemListCreateView.as_view(), name='menuitem-list-create'),
    path('categories/<int:category_id>/menu-items/', MenuItemsByCategoryView.as_view()),
    path('menu-items/<int:pk>/', MenuItemRetrieveUpdateDeleteView.as_view(), name='menuitem-detail'),
]
