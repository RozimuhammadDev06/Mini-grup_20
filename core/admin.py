from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Category, Brand, Branch, User, Product,
    Address, Order, OrderProduct, Cart, CartProduct,
    Review, Wishlist, Promotion, News
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'created')
    list_filter = ('active',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active', 'crated')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_staff')
    search_fields = ('username', 'email', 'phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'discount', 'is_active', 'crated_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'desc')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'city', 'is_default')
    list_filter = ('is_default', 'city')
    search_fields = ('full_name', 'city', 'address')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'payment_status', 'crated_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('user__username', 'id')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'crated_at')

@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'price')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'crated_at')
    list_filter = ('rating',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'crated_at')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'discount_percent', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')