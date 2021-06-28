
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from . import serializers
from .models import Product, Category, Like, Favorite
from .serializers import FavoriteSerializer


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminUser, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAdminUser, ]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAdminUser, )


class ProductListView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        product = self.get_object()
        obj, created = Like.objects.get_or_create(owner=request.user, product=product)
        if not created:
            obj.like = not obj.like
            obj.save()
        liked_or_unliked = 'liked' if obj.like else 'unliked'
        return Response('Successfully {} product'.format(liked_or_unliked), status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        product = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.favorite = not obj.favorite
            print(obj.favorite)
            obj.save()
        added_removed = 'added' if obj.favorite else 'removed'
        return Response('Successfully {} favorite'.format(added_removed), status=status.HTTP_200_OK)


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        qs = self.request.user
        queryset = Favorite.objects.filter(user=qs, favorite=True)
        return queryset
