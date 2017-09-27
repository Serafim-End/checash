
import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from bill.serializers import BillSerializer
from bill.service import BillService
from bill.models import Bill
from promo.serializers import PromoSerializer
from promo.service import PromoService
from categorizer.categorizer import categorizer

from .models import Person
from .serializers import PersonSerializer


class PersonViewSet(ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # renderer_classes = (JSONRenderer, )

    @detail_route(methods=['post'], url_path='add-bill')
    def add_bill(self, request, pk=None):
        """

        :param request: should contain the data in bill serializer format
        :param pk:
        :return: Person Serialized format of person instance
        and errors otherwise
        """
        person = self.get_object()
        bill_info = BillService.get_info(request.data)
        serializer = BillSerializer(data=bill_info)

        if serializer.is_valid():
            bill_instance = serializer.save()
            person.bills.add(bill_instance)
            person.save()
            return Response(PersonSerializer(person).data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post', 'get'], url_path='get-bonus')
    def get_bonus(self, request, pk=None):
        """

        :param request:
        POST to reset cashback
        GET  to return current cashback
        :param pk:
        :return: POST - {}, GET - current cashback
        """

        person = self.get_object()

        if request.method == 'POST':
            person.current_cashback = 0
            person.save()
            return Response(status=status.HTTP_200_OK)

        elif request.method == 'GET':
            return Response(json.dumps(person.current_cashback),
                            status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='get-all-time-bonus')
    def get_all_time_bonus(self, request, pk=None):
        """

        :param request: no special info
        :param pk:
        :return: info about whole cashback through application
        """
        person = self.get_object()

        return Response(json.dumps(person.total_cashback),
                        status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='get-bills-detailed')
    def get_bill_detailed(self, request, pk=None):
        """

        :param request: no special data
        :param pk:
        :return: {serialized detailed info about person`s bills}
        """

        person = self.get_object()

        return Response(BillSerializer(person.bills.all(), many=True).data,
                        status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='get-bills')
    def get_bills(self, request, pk=None):
        """

        :param request: no special data
        :param pk:
        :return: {serialized info about person`s bills}
        """

        person = self.get_object()

        important_fields = ('fiscalSign', 'cashback',
                            'total_sum', 'in_processing')

        data = []
        for i, bill in enumerate(person.bills.all()):
            data.append({})
            for f in important_fields:
                data[-1][f] = getattr(bill, f)
        print(json)
        return Response(data, status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='get-statistics')
    def get_statistics(self, request, pk=None):

        person = self.get_object()

        data = {}
        for bill in person.bills.all():

            for item in bill.items.all():

                r = categorizer.get_categories_hierarchy(
                    item.name
                )

                if len(r) == 0:
                    h_1, h_2, cat_id = u'Другие', u'совсем другие', -1
                
                else:
                    h_1, h_2, cat_id = r

                if cat_id not in data:
                    data[cat_id] = {'name': ' '.join([h_1, h_2]),
                                    'sum': 0,
                                    'items': []}

                data[cat_id]['items'].append(item.name)
                data[cat_id]['sum'] += item.price

        return Response(data, status=status.HTTP_200_OK)

    @detail_route(methods='get',
                  url_path='get-bill-promos/(?P<bill_id>[0-9]+)')
    def get_bill_promos(self, request, pk=None, bill_id=None):
        person = self.get_object()

        if not bill_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        o = Bill.objects.filter(fiscalSign=bill_id)

        if o not in person.bills.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if o.count() == 1:

            active_promos = PromoService.get_active_promos()

            data = {}
            for item in o.items.all():
                for promo in item.promos.all():
                    if promo in active_promos:
                        data[item.id] = PromoSerializer(promo)

            return Response(json.dumps(data), status=status.HTTP_200_OK)
