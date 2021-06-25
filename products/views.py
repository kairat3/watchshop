from rest_framework.filters import SearchFilter
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from . import serializers
from .models import Product, Category


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
    permission_classes = (permissions.AllowAny, )
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    filterset_fields = ('title', 'category', )


class ProductDetailView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.AllowAny, )


class ProductCreateView(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser, )


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser, )


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAdminUser, )
