from rest_framework import serializers
from .models import Product, Review


from .models import (
    Address,
    Item,
    News,
    Order,
    OrderItem,
    Promotion,
    Review,
    User,
    Wishlist,
)

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'crated_at']

    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "username", "product", "rating", "comment", "crated_at"]
        read_only_fields = ["id", "username", "crated_at"]

    def validate(self, attrs):
        request = self.context["request"]
        # Yaratishda: bitta tovarga bitta otziv
        if self.instance is None:
            if Review.objects.filter(user=request.user, product=attrs["product"]).exists():
                raise serializers.ValidationError("Siz bu tovarga allaqachon otziv qoldirgansiz.")
        # Tahrirlashda tovarni almashtirib bo'lmaydi
        elif "product" in attrs and attrs["product"] != self.instance.product:
            raise serializers.ValidationError({"product": "Tovarni o'zgartirib bo'lmaydi."})
        return attrs

class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'brand_name', 'desc', 'price', 'discount', 'is_active', 'reviews', 'crated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CategorySerializer:
    pass


class BrandSerializer:
    pass


# ---------- 1. User profil ----------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "username", "created_at", "updated_at"]

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value).exclude(pk=self.instance.pk)
        if value and qs.exists():
            raise serializers.ValidationError("Bu email allaqachon band.")
        return value


# ---------- Item (qisqa ko'rinish) ----------
class ItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "price", "discount", "is_active"]


# ---------- 4. Dostavka manzili ----------
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "full_name", "phone", "address", "city",
            "region", "postal_code", "is_default", "crated_at",
        ]
        read_only_fields = ["id", "crated_at"]


# ---------- 2. Zakazlar ----------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ItemShortSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "discount"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "status", "address", "total_amount", "payment_method",
            "payment_status", "items", "crated_at", "updated_at",
        ]


# ---------- 3. Wishlist ----------
class WishlistSerializer(serializers.ModelSerializer):
    product = ItemShortSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.filter(is_active=True),
        source="product",
        write_only=True,
    )

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_id", "crated_at"]
        read_only_fields = ["id", "crated_at"]

    def validate_product_id(self, product):
        user = self.context["request"].user
        if Wishlist.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Bu tovar allaqachon sevimlilarda.")
        return product


# ---------- 5. Otziv (Review) ----------
def validate_rating(value):
    if not 1 <= value <= 5:
        raise serializers.ValidationError("Reyting 1 dan 5 gacha bo'lishi kerak.")
    return value

# ---------- 6. Aksiya ----------
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            "id", "title", "description", "image",
            "discount_percent", "start_date", "end_date",
        ]


# ---------- 7. News ----------
class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "slug", "image", "created_at"]


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "slug", "content", "image", "created_at"]