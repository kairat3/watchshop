from rest_framework import serializers

from like.models import Like
from products.models import Product, Category, PostImages
from review.models import Review
from review.serializers import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
        return representation


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'available', 'preview']

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        created_product = Product.objects.create(**validated_data)
        images_obj = [
            PostImages(post=created_product, image=image) for image in images_data.getlist('images')
        ]
        PostImages.objects.bulk_create(images_obj)
        return created_product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['review_count'] = f'{Review.objects.filter(product=instance.id).count()}'
        representation['like_count'] = f'{Like.objects.filter(post=instance.id).count()}'
        return representation


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['review'] = ReviewSerializer(Review.objects.filter(product=instance.id), many=True).data
        # representation['likes'] = LikeSerializer(Like.objects.filter(food=instance.id), many=True).data
        return representation
