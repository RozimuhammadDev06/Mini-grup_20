from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCompareView, home_page_view, ChangePasswordView
)

urlpatterns = [
    path('home/', home_page_view, name='home-page'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/compare/', ProductCompareView.as_view(), name='product-compare'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
