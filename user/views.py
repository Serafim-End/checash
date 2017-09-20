
import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from bill.serializers import BillSerializer

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
    def get_bill_detailed(self):

        person = self.get_object()

        return Response(BillSerializer(person.bills, many=True),
                        status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='get-bills')
    def get_bill_detailed(self):

        person = self.get_object()

        important_fields = ('fiscalSign', 'dateTime', 'cashback',
                            'total_sum', 'in_processing')

        data = []
        for i, bill in enumerate(person.bills):
            data.append({})
            for f in important_fields:
                data[-1][f] = getattr(bill, f)

        return Response(json.dumps(data), status.HTTP_200_OK)