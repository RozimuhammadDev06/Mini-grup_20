from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers


from .models import (
    Address,
    Brand,
    Category,
    News,
    Order,
    OrderProduct,  # Sizda OrderItem o'rniga OrderProduct ishlatilgan
    Product,
    Promotion,
    Review,
    Wishlist,
)





User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User  # <--- Shu yerda model aniq ko'rsatilgan bo'lishi shart!
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
        )
        return user

# ---------- 2. Review Serializer ----------
class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "username", "product", "rating", "comment", "crated_at"]
        read_only_fields = ["id", "username", "crated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.method == "POST" and self.instance is None:
            if Review.objects.filter(user=request.user, product=attrs["product"]).exists():
                raise serializers.ValidationError("Siz bu tovarga allaqachon otziv qoldirgansiz.")
        elif "product" in attrs and self.instance and attrs["product"] != self.instance.product:
            raise serializers.ValidationError({"product": "Tovarni o'zgartirib bo'lmaydi."})
        return attrs


# ---------- 3. Product Serializers ----------
class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'desc', 'price', 'discount', 'is_active', 'reviews', 'crated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# ---------- 4. Category & Brand Serializers ----------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'active', 'created']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'is_active', 'crated']


# ---------- 5. Change Password Serializer ----------
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# ---------- 6. User Profile Serializer ----------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "username", "created_at", "updated_at"]

    def validate_email(self, value):
        if self.instance and value:
            qs = User.objects.filter(email__iexact=value).exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Bu email allaqachon band.")
        return value


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "full_name", "phone", "address", "city",
            "region", "postal_code", "is_default", "crated_at",
        ]
        read_only_fields = ["id", "crated_at"]


# ---------- 8. Order Serializers ----------
class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ["id", "product", "quantity", "price", "discount", "crated_at"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "status", "address", "total_amount", "payment_method",
            "payment_status", "products", "crated_at", "updated_at",
        ]


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source="product",
        write_only=True,
    )

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_id", "crated_at"]
        read_only_fields = ["id", "crated_at"]

    def validate_product_id(self, product):
        request = self.context.get("request")
        if request and Wishlist.objects.filter(user=request.user, product=product).exists():
            raise serializers.ValidationError("Bu tovar allaqachon sevimlilarda.")
        return product


# ---------- 10. Promotion Serializer ----------
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            "id", "title", "description", "image",
            "discount_percent", "start_date", "end_date",
        ]


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "slug", "image", "created_at"]


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "slug", "content", "image", "created_at"]