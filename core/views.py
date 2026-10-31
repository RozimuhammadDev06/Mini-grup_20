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