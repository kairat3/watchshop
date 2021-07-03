from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ('body', 'product', 'owner')

    def to_representation(self, instance):
        representation = super(ReviewSerializer, self).to_representation(instance)
        representation['owner'] = instance.owner.email
        print(f'11111{representation}')
        return representation