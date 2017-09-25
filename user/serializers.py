
from rest_framework.serializers import ModelSerializer

# from bill.serializers import BillSerializer

from .models import Person


class PersonSerializer(ModelSerializer):

    # bills = BillSerializer(many=True)

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'bills', 'username')
