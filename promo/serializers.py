
from rest_framework import serializers

from .models import Promo

# from items.serializers import ItemSerializer


class PromoSerializer(serializers.ModelSerializer):

    # items = ItemSerializer(many=False)
    url = serializers.CharField(read_only=True, source='items.url')
    description = serializers.CharField(read_only=True,
                                        source='items.description')

    class Meta:
        model = Promo
        fields = ('title', 'due_date', 'start_date', 'cashback_rub',
                  'lower_bound_rub', 'url', 'description')
