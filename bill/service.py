
import requests


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
