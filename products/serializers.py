from rest_framework import serializers

from like.models import Like
from products.models import Product, Category, PostImages


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
        fields = '__all__'

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
        representation['like_count'] = f'{Like.objects.filter(id=instance.id).count()}'
        return representation
