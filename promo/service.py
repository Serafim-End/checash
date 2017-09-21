
import datetime

from .models import Promo


class PromoService(object):

    @staticmethod
    def get_active_promos():
        """
        data about active promos

        :return: QuerySet
        """

        today = datetime.datetime.today()

        queryset = Promo.objects.filter(
            start_date__gt=today,
            due_date__lt=today
        )

        return queryset
