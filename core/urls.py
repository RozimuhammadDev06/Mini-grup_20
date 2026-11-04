from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ProductListView, ProductDetailView,
    ProductCompareView, home_page_view, ChangePasswordView,
    RegisterView, LogoutView, CategoryListView,
    ProfileView, PromotionListView,
    OrderViewSet, WishlistViewSet, AddressViewSet, ReviewViewSet, NewsViewSet,
    CustomObtainAuthToken  # <--- Shu yerda import qilingan
)

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("wishlist", WishlistViewSet, basename="wishlist")
router.register("addresses", AddressViewSet, basename="address")
router.register("reviews", ReviewViewSet, basename="review")
router.register("news", NewsViewSet, basename="news")

urlpatterns = [
    path('home/', home_page_view, name='home-page'),
    path('products/', ProductListView.as_view(), name='product-list'),

    # Compare doim <int:pk> dan oldin turishi kerak
    path('products/compare/', ProductCompareView.as_view(), name='product-compare'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Faqat bitta va to'g'ri CustomObtainAuthToken ishlatiladi:
    path("auth/token/", CustomObtainAuthToken.as_view(), name="token"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path("promotions/", PromotionListView.as_view(), name="promotions"),
    path("", include(router.urls)),
]