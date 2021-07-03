from rest_framework import serializers

from products.models import Product, Category, PostImages, Favorite, Like, Bag
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
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'preview', 'likes', 'review')

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        action = self.context.get('action')
        request = self.context.get('request')
        likes = LikeSerializer(instance.likes.filter(like=True), many=True).data
        # reviews = ReviewSerializer(instance.review.all()).data
        if action == 'list':
            representation['likes'] = {'like': likes}
            representation['likes'] = instance.likes.filter(like=True).count()
            print(representation)
        # if action == 'retrieve':
            # representation['review'] = reviews
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


class BagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bag
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        review = Bag.objects.create(user=user, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(BagSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation
