
import traceback

from rest_framework import serializers

from items.serializers import ItemSerializer
from items.models import Item

from .models import Bill


class BillSerializer(serializers.ModelSerializer):

    qr = serializers.JSONField()
    items = ItemSerializer(many=True)

    class Meta:
        model = Bill
        fields = ('dateTime', 'nds18', 'taxation_type',
                  'ecash_total_sum', 'qr', 'fiscalSign',
                  'cashTotalSum', 'total_sum', 'operationType', 'items')

    def create(self, validated_data):
        """
        without data validation - need only qr code
        :param validated_data:
        :return:
        """

        items_data = validated_data.pop('items')

        model_class = self.Meta.model

        try:
            instance = model_class.objects.create(**validated_data)
        except TypeError:
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                '\nOriginal exception was:\n %s' %
                (
                    model_class.__name__,
                    traceback.format_exc()
                )
            )
            raise TypeError(msg)

        for item_data in items_data:
            item, created = Item.objects.get_or_create(
                **item_data
            )

            instance.items.add(item)

        instance.determine_cashback()

        return instance
