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
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = StandardResultsSetPagination


class ProductCreateView(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )
