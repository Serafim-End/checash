
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from checash.settings import client

from .serializers import BillSerializer


class BillView(APIView):

    def post(self, request, format=None):

        # nice example
        # fn = 8710000100239499 & i = 36082 & fp = 1134274756 & n = 1

        data = request.data

        _g = lambda n: data.get(n)

        fn, i, fp, n = _g('fn'), _g('i'), _g('fp'), _g('n')



        BillSerializer(**data)

        if 'user_id' not in data:
            return Response('user_id address should be in request',
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = data.get('user_id')
        except Exception as e:
            client.captureException(exc_info='400')

            return Response(
                'error during user_id parsing: {}'.format(e.message),
                status=status.HTTP_400_BAD_REQUEST
            )

        user = user_getter(user_id=user_id)
        if user.friends.count() == 0:
            return Response('No friends were found for this user',
                            status=status.HTTP_404_NOT_FOUND)

        friends_ids = json.dumps(
            {
                'friends': [f.kinohod_id for f in user.friends.all()]
            }
        )

        return Response(data=friends_ids, status=status.HTTP_200_OK)