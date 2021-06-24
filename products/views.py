from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from . import serializers
from .models import Product, Category
from django_filters import rest_framework as filters


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAdminUser, )


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filters_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('title', 'price', 'category')
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(id__icontains=search) | Q(price__icontains=search)
            )
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductRetrieveSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.AllowAny, )


class ProductCreateView(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )
