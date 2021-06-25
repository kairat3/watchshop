from rest_framework import serializers

from products.models import Product
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ('id', 'body', 'owner', 'product')

