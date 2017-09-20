
import datetime

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from .models import Promo
from .serializers import PromoSerializer


class PromoViewSet(viewsets.ModelViewSet):

    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

    @detail_route(methods=['post'], url_path='get-promos')
    def get_promos(self):

        today = datetime.datetime.today()

        queryset = Promo.objects.filter(
            start_date__gt=today,
            due_date__lt=today
        )

        return Response(PromoSerializer(queryset.all(), many=True),
                        status=status.HTTP_200_OK)
