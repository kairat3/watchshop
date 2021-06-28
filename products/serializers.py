from rest_framework import serializers

from products.models import Product, Category, PostImages, Favorite, Like


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
        return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('owner', 'like')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.email
        return representation


class ProductSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'preview', 'likes',)

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        action = self.context.get('action')
        likes = LikeSerializer(instance.likes.filter(like=True), many=True).data
        if action == 'list':
            representation['likes'] = {'like': likes}
            representation['likes'] = instance.likes.filter(like=True).count()
        if action == 'retrieve':
            representation['likes'] = likes
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        review = Favorite.objects.create(user=user, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(FavoriteSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation


# class ProductSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         images_data = request.FILES
#         created_product = Product.objects.create(**validated_data)
#         images_obj = [
#             PostImages(post=created_product, image=image) for image in images_data.getlist('images')
#         ]
#         PostImages.objects.bulk_create(images_obj)
#         return created_product
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['like_count'] = Like.objects.filter(id=instance.id).count()
#         return representation
