from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ProductSerializer, ProductDetailSerializer, ChangePasswordSerializer
from .filters import ProductFilter
from rest_framework.decorators import api_view
from .models import Category, Product, Brand
from .serializers import CategorySerializer, ProductSerializer, BrandSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView




from django.db import transaction
from django.utils import timezone
from rest_framework import mixins, permissions, viewsets
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from .models import Address, News, Order, Promotion, Review, Wishlist
from .serializers import (
    AddressSerializer,
    NewsDetailSerializer,
    NewsListSerializer,
    OrderSerializer,
    PromotionSerializer,
    ReviewSerializer,
    UserProfileSerializer,
    WishlistSerializer,
)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'desc']
    ordering_fields = ['price', 'crated_at']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductCompareView(APIView):
    def get(self, request):
        product_ids = request.query_params.get('ids', '')
        if not product_ids:
            return Response({"error": "Mahsulot ID lari berilmadi (ids=1,2,3)"}, status=400)

        ids = [int(i) for i in product_ids.split(',') if i.isdigit()]
        products = Product.objects.filter(id__in=ids)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def home_page_view(request):
    categories = Category.objects.filter(active=True)[:10]
    new_products = Product.objects.filter(is_active=True).order_by('-crated_at')[:10]
    popular_products = Product.objects.filter(is_active=True)[:10] # yoki ko'rishlar/sotuvlar soniga qarab
    brands = Brand.objects.filter(is_active=True)[:10]

    return Response({
        "categories": CategorySerializer(categories, many=True).data,
        "new_products": ProductSerializer(new_products, many=True).data,
        "popular_products": ProductSerializer(popular_products, many=True).data,
        "brands": BrandSerializer(brands, many=True).data,
    })


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Eski parol noto'g'ri."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"detail": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ---------- Permission ----------
class IsOwnerOrReadOnly(permissions.BasePermission):
    """O'qish hamma uchun, o'zgartirish/o'chirish faqat egasi uchun."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


# ---------- 1. User profil: GET / PUT / PATCH /api/profile/ ----------
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "put", "patch", "head", "options"]

    def get_object(self):
        return self.request.user


# ---------- 2. User zakazlari: GET /api/orders/ , /api/orders/{id}/ ----------
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .select_related("address")
            .prefetch_related("items__product")
            .order_by("-crated_at")
        )


# ---------- 3. Wishlist: GET, POST, DELETE /api/wishlist/ ----------
class WishlistViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Wishlist.objects.filter(user=self.request.user)
            .select_related("product")
            .order_by("-crated_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- 4. Dostavka manzili: to'liq CRUD /api/addresses/ ----------
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by("-is_default", "-crated_at")

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        # Birinchi manzil avtomatik asosiy bo'ladi
        if not Address.objects.filter(user=user).exists():
            serializer.validated_data["is_default"] = True
        address = serializer.save(user=user)
        self._ensure_single_default(address)

    @transaction.atomic
    def perform_update(self, serializer):
        address = serializer.save()
        self._ensure_single_default(address)

    @staticmethod
    def _ensure_single_default(address):
        """Faqat bitta manzil asosiy (is_default) bo'lib qolishini ta'minlaydi."""
        if address.is_default:
            Address.objects.filter(user=address.user).exclude(pk=address.pk).update(is_default=False)


# ---------- 5. Otziv (Review): CRUD /api/reviews/?product=<id> ----------
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Review.objects.select_related("user", "product").order_by("-crated_at")
        product_id = self.request.query_params.get("product")
        if product_id:
            qs = qs.filter(product_id=product_id)
        # Ro'yxatda faqat o'zimnikini ko'rish: ?mine=1
        if self.request.query_params.get("mine") and self.request.user.is_authenticated:
            qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- 6. Aksiya: GET /api/promotions/ ----------
def get_queryset():
    now = timezone.now()
    return Promotion.objects.filter(
        is_active=True, start_date__lte=now, end_date__gte=now
    )


class PromotionListView(ListAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]


# ---------- 7. News: GET /api/news/ , /api/news/{slug}/ ----------
class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get_serializer_class(self):
        return NewsListSerializer if self.action == "list" else NewsDetailSerializer






