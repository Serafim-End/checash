
import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from bill.serializers import BillSerializer
from bill.models import Bill
from promo.serializers import PromoSerializer

from .models import Person
from .serializers import PersonSerializer


class PersonViewSet(ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @detail_route(methods=['post'], url_path='add-bill')
    def add_bill(self, request, pk=None):
        person = self.get_object()
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            bill_instance = serializer.save()
            person.bills.add(bill_instance)
            person.save()
            return Response(PersonSerializer(person),
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post', 'get'], url_path='get-bonus')
    def get_bonus(self, request, pk=None):

        person = self.get_object()

        if request.method == 'post':
            person.current_cashback = 0
            person.save()
            return Response(status=status.HTTP_200_OK)

        elif request.method == 'get':
            return Response(json.dumps(person.current_cashbac),
                            status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def get_all_time_bonus(self, request, pk=None):

        person = self.get_object()

        return Response(json.dumps(person.total_cashback),
                        status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='get-bills-detailed')
    def get_bill_detailed(self, request, pk=None):

        person = self.get_object()

        return Response(BillSerializer(person.bills.all(), many=True),
                        status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='get-bills')
    def get_bill_detailed(self, request, pk=None):

        person = self.get_object()

        important_fields = ('fiscalSign', 'dateTime', 'cashback',
                            'total_sum', 'in_processing')

        data = []
        for i, bill in enumerate(person.bills.all()):
            data.append({})
            for f in important_fields:
                data[-1][f] = getattr(bill, f)

        return Response(json.dumps(data), status.HTTP_200_OK)

    @detail_route(methods='get',
                  url_path='get-bill-promos/(?P<bill_id>[0-9]+)')
    def get_bill_promos(self, request, pk=None, bill_id=None):
        person = self.get_object()

        if not bill_id:
            data = {}
            for bill in person.bills.all():
                data[bill.fiscalSign] = PromoSerializer(
                    bill.promos.all(), many=True
                )

            return Response(json.dumps(data), status=status.HTTP_200_OK)

        o = Bill.objects.filter(fiscalSign=bill_id)
        if o.count() == 1:
            return Response(PromoSerializer(o.promos.all(), many=True),
                            status=status.HTTP_200_OK)
