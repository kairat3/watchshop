from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters import rest_framework as filters
from . import serializers
from .models import Product, Category, Like, Favorite, Bag
from .serializers import FavoriteSerializer
from django.db.models import Q


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
    filters_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('title', 'price', 'category')

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(id__icontains=search) | Q(price__icontains=search))
        return queryset


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

    @action(detail=True, methods=['post'])
    def bag(self, request, pk=None):
        product = self.get_object()
        obj, created = Bag.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.in_bag = not obj.in_bag
            print(obj.in_bag)
            obj.save()
        added_removed = 'added to' if obj.in_bag else 'removed from'
        return Response('Successfully {} bag'.format(added_removed), status=status.HTTP_200_OK)


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        qs = self.request.user
        queryset = Favorite.objects.filter(user=qs, favorite=True)
        return queryset


class BagListView(generics.ListAPIView):
    queryset = Bag.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Bag.objects.none()
        qs = self.request.user
        queryset = Bag.objects.filter(user=qs, in_bag=True)
        return queryset

