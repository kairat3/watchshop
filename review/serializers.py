from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ('id', 'body', 'owner', 'product')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        review = Review.objects.create(owner=user, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(ReviewSerializer, self).to_representation(instance)
        representation['owner'] = instance.owner.email
        return representation
