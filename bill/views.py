
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BillSerializer
from .service import BillService


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

        bill_info = BillService.get_info(data)

        serializer = BillSerializer(data=bill_info)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
