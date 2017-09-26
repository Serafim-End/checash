import re
from datetime import datetime, timedelta

import requests

from lxml import html

from items.models import Item

from .models import Promo

from .settings import *


class PromoService(object):
    @staticmethod
    def get_active_promos():
        """
        data about active promos

        :return: QuerySet
        """

        today = datetime.today()

        queryset = Promo.objects.filter(
            start_date__gt=today,
            due_date__lt=today
        )

        return queryset

    @staticmethod
    def dixy():

        DATE_FORMAT = '%d.%m.%Y'

        def _p(p):
            return parsed_body.xpath(p)

        def _str(l):
            print(l)
            return l.encode('utf-8').decode('utf-8')

        def _d(d):
            return datetime.strptime(d.pop(), DATE_FORMAT)

        response = requests.get(BASE_DISCOUNT_URL)
        parsed_body = html.fromstring(response.text)

        for i in xrange(len(_p(PATH_WHOLE_CONTENT))):

            title = _str(_p(PATH_TITLE)[i])
            data = re.findall(r'\d{2}.\d{2}.\d{2,4}', title)

            if len(data) == 0:
                _start = datetime.today()
                _end = _start + timedelta(days=1)

            elif len(data) == 1:
                _start = datetime.today()
                _end = _d(data)

            else:
                _end, _start = _d(data), _d(data)

            yield {
                'name': _str(_p(PATH_NAME)[i]),
                'url': '{}{}'.format(BASE_URL, _str(_p(PATH_PHOTO)[i])),
                'price_new': int(_str(_p(PATH_PRICE_NEW)[i])),
                'price_old': int(_str(_p(PATH_PRICE_OLD)[i])),
                'title': title,
                'start': _start,
                'end': _end,
                'promo': _str(_p(PATH_PROMO)[i])

            }

    @staticmethod
    def dixy_skidki_nedeli():

        DATE_FORMAT = '%d.%m.%Y'


        def _p(p):
            return parsed_body.xpath(p)

        def _str(l):
            print(l)
            return l.encode('utf-8').decode('utf-8')

        def _d(d):
            return datetime.strptime(d.pop(), DATE_FORMAT)

        j = 0
        page_id = 1
        page_active = 1

        while page_id - page_active <= 3:
            page = BASE_DISCOUNT_URL_DIXY_SKIDKI_NEDELI + str(page_id)
            response = requests.get(page)
            
            parsed_body = html.fromstring(response.text)
            page_active = int(_p(PATH_ACTIVE_PAGE_NUMBER)[0])

            if page_active == page_id:

                for i in xrange(len(_p(PATH_WHOLE_CONTENT_DIXY_SKIDKI_NEDELI))):
                    title = _str(_p(PATH_WHOLE_CONTENT_DIXY_SKIDKI_NEDELI)[i])

                    data = re.findall(r'\d{2}/\d{2}', title)

                    if len(data) == 0:
                        _start = datetime.today()
                        _end = _start + timedelta(days=1)

                    elif len(data) == 1:
                        _start = datetime.today()
                        data = data[0] + '/' + str(datetime.now().year)
                        _end = _d(data)
                    else:
                        data = data + '/' + str(datetime.now().year), data + '/' + str(datetime.now().year)
                        _end, _start = _d(data), _d(data)

                    j = i * 4 - 1
                    category = _str(_p(PATH_CATEGORY_DIXY_SKIDKI_NEDELI)[j])

                    price_new = int(_str(_p(PATH_PRICE_NEW_DIXY_SKIDKI_NEDELI)[i]))

                    price_old = _p(PATH_PRICE_OLD_DIXY_SKIDKI_NEDELI)[i]

                    if not price_old.isdigit():
                        price_old = price_new / 0.9

                    yield {
                            'name': _str(_p(PATH_NAME_DIXY_SKIDKI_NEDELI)[i]),
                            'url': '{}{}'.format(BASE_URL, _str(_p(PATH_NAME_DIXY_SKIDKI_NEDELI)[i])),
                            'price_new': price_new,
                            'price_old': int(price_old),
                            'title': title,
                            'start': _start,
                            'end': _end,
                            'promo': ''
                        } \


            else:
                break
            page_id += 1

    @staticmethod
    def combine():
        yield from PromoService.dixy_skidki_nedeli()
        yield from PromoService.dixy()

    @staticmethod
    def get_actual_promos():

        promos = []

        for e in PromoService.combine():

            item = Item.objects.create(
                name=e.get('name'),
                url=e.get('url'),
                price=int(e.get('price_new')),
                cashback=0
            )

            promo = Promo.objects.create(
                cashback_rub=abs(e.get('price_new') - e.get('price_old')),
                title=e.get('title'),
                lower_bound_rub=e.get('price_new'),
                due_date=e.get('end'),
                start_date=e.get('start')
            )

            promo.items = item

            promos.append(promo)


        return promos
