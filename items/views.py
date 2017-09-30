
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from categorizer.categorizer import categorizer

from items.models import Item
from items.serializers import ItemSerializer


class ItemViewSet(ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @detail_route(methods=['get'], url_path='category')
    def get_category(self, request, pk=None):

        item = self.get_object()

        r = categorizer.get_categories_hierarchy(
            item.name
        )

        if len(r) == 0:
            h_1, h_2, cat_id = u'Другие', u'совсем другие', -1

        else:
            h_1, h_2, cat_id = r

        return Response(
            {'h_1': h_1, 'h_2': h_2, 'cat_id': cat_id},
            status=status.HTTP_200_OK
        )
