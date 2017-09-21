
import requests

from promo.service import PromoService


class BillService(object):

    """
    in this module we are trying to get info from the bill by the qr code

    qr code -> state tax service -> bill info to our db
    """

    BASE_URL = 'https://qrtests.herokuapp.com/receipts/get'

    @staticmethod
    def get_info(data):

        _g = lambda n: data.get(n)

        fn, i, fp, n = _g('fn'), _g('i'), _g('fp'), _g('n')
        qr = {'fn': fn, 'i': i, 'fp': fp, 'n': n}

        r = requests.get(
            BillService.BASE_URL,
            params=qr
        )

        json_result = r.json()

        if json_result.get('fiscalDocumentNumber'):
            json_result['qr'] = qr
            return json_result

        else:
            data = {'qr': qr}

    @staticmethod
    def determine_cashback(self, instance):

        active_promos = PromoService.get_active_promos()

        # the case just for one item in promo
        for item in instance.items.all():
            for promo in active_promos.all():
                if (item in promo.items and
                        instance.total_sum >= promo.lower_bound_rub):
                    instance.cashback += promo.cashback_rub

        instance.save()
