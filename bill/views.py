
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BillSerializer
from .service import BillService
from .models import Bill


class BillView(APIView):

    def post(self, request, format=None):
        """

        :param request: contains data that contain no less than 4 fields
        (fn, i, fp and n) that are required to get info from the bill

        nice example
        fn = 8710000100239499 & i = 36082 & fp = 1134274756 & n = 1

        :param format:
        :return: serialized data from our model
        """

        data = request.data

        qr = BillService.prepare_data(data)

        queryset = Bill.objects.filter(fiscalSign=qr.get('fp'))
        if not queryset.count():

            bill_info = BillService.get_info(qr)
            serializer = BillSerializer(data=bill_info)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(data=BillSerializer(queryset.all(), many=True).data,
                        status=status.HTTP_200_OK)


class BillFPView(APIView):

    def get(self, request, format=None):

        data = request.data

        fp = data.get('fp')

        if not fp:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        q = Bill.objects.filter(fiscalSign=fp)

        if not q.count():
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            BillSerializer(q.all(), many=True).data,
            status=status.HTTP_200_OK
        )
