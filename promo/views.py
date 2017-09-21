
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from .models import Promo
from .service import PromoService
from .serializers import PromoSerializer


class PromoViewSet(viewsets.ModelViewSet):

    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

    @detail_route(methods=['post'], url_path='get-promos')
    def get_promos(self):

        queryset = PromoService.get_active_promos()

        return Response(PromoSerializer(queryset.all(), many=True),
                        status=status.HTTP_200_OK)
