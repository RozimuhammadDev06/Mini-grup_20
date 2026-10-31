from django.urls import include, path
from .views import (
    ProductListView, ProductDetailView,
    ProductCompareView, home_page_view, ChangePasswordView
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("wishlist", WishlistViewSet, basename="wishlist")
router.register("addresses", AddressViewSet, basename="address")
router.register("reviews", ReviewViewSet, basename="review")
router.register("news", NewsViewSet, basename="news")




urlpatterns = [
    path('home/', home_page_view, name='home-page'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/compare/', ProductCompareView.as_view(), name='product-compare'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path("auth/token/", obtain_auth_token, name="token"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("promotions/", PromotionListView.as_view(), name="promotions"),
    path("", include(router.urls)),
]
