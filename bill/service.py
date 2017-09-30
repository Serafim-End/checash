
import requests

from promo.service import PromoService


class BillService(object):

    """
    in this module we are trying to get info from the bill by the qr code

    qr code -> state tax service -> bill info to our db
    """

    BASE_URL = 'https://qrtests.herokuapp.com/receipts/get'

    @staticmethod
    def prepare_data(data):

        qr_data = data.get('qr')

        if qr_data:
            qr = {}
            for e in qr_data.split('&'):
                k, v = e.split('=')
                if k in ('fn', 'i', 'fp', 'n'):
                    qr[k] = v

        else:
            _g = lambda n: data.get(n)

            fn, i, fp, n = _g('fn'), _g('i'), _g('fp'), _g('n')
            qr = {'fn': fn, 'i': i, 'fp': fp, 'n': n}

        return qr

    @staticmethod
    def get_info(qr):

        try:
            r = requests.get(
                BillService.BASE_URL,
                params=qr
            )
        except Exception:
            return {'qr': qr}

        json_result = r.json()

        if json_result.get('fiscalDocumentNumber'):
            json_result['qr'] = qr
            return json_result

        else:
            return {'qr': qr}

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
