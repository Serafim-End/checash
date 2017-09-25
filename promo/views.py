
import json

from rest_framework import viewsets, views

from rest_framework.response import Response
from rest_framework import status

from .models import Promo
from .service import PromoService
from .serializers import PromoSerializer


class PromoViewSet(viewsets.ModelViewSet):

    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


class PublicPromos(views.APIView):

    def get(self, request, format=None):

        promos = PromoService.get_actual_promos()
        return Response(PromoSerializer(promos, many=True).data,
                        status=status.HTTP_200_OK)
