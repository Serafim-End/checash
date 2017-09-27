
from rest_framework.serializers import ModelSerializer

# from promo.serializers import PromoSerializer

from .models import Item


class ItemSerializer(ModelSerializer):

    # items = PromoSerializer(many=True)

    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'url')
