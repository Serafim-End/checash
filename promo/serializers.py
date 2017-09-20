
import traceback

from rest_framework import serializers

from items.serializers import ItemSerializer

from .models import Promo


class PromoSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = Promo
        fields = ('title', 'due_date', 'start_date', 'cashback_rub',
                  'items', 'lower_bound_rub')
