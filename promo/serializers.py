
from rest_framework import serializers

from .models import Promo

from items.serializers import ItemSerializer


class PromoSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=False)

    class Meta:
        model = Promo
        fields = ('title', 'due_date', 'start_date', 'cashback_rub',
                  'items', 'lower_bound_rub')
