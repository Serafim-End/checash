
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

    def _p(self, parsed_body, p):
        return parsed_body.xpath(p)

    def _str(self, l):
        return l.encode('utf-8').decode('utf-8')

    def _d(self, d, date_format, add_year=False, **kwargs):
        if add_year:
            now = kwargs.get('now', datetime.now())
            return datetime.strptime(
                '{}{}{}'.format(d.pop(), '/', now.year),
                date_format
            )

        return datetime.strptime(d.pop(), date_format)

    def dixy(self):

        date_format = '%d.%m.%Y'

        response = requests.get(BASE_DISCOUNT_URL)
        pb = html.fromstring(response.text)

        for i in range(len(self._p(pb, PATH_WHOLE_CONTENT))):

            title = self._str(self._p(pb, PATH_TITLE)[i])
            data = re.findall(r'\d{2}.\d{2}.\d{2,4}', title)

            if len(data) == 0:
                _start = datetime.today()
                _end = _start + timedelta(days=1)

            elif len(data) == 1:
                _start = datetime.today()
                _end = self._d(data, date_format)

            else:
                _end, _start = (self._d(data, date_format),
                                self._d(data, date_format))

            yield {
                'name': self._str(self._p(pb, PATH_NAME)[i]),

                'url': '{}{}'.format(
                    BASE_URL,
                    self._str(self._p(pb, PATH_PHOTO)[i])
                ),

                'price_new': int(self._str(self._p(pb, PATH_PRICE_NEW)[i])),
                'price_old': int(self._str(self._p(pb, PATH_PRICE_OLD)[i])),
                'title': title,
                'start': _start,
                'end': _end,
                'promo': self._str(self._p(pb, PATH_PROMO)[i])
            }

    def parse_page(self, pb):
        date_format = '%d/%m/%Y'

        item_counts = len(self._p(pb, PATH_WHOLE_CONTENT_DIXY_SKIDKI_NEDELI))

        now = datetime.now()

        # category_i = 0

        for i in range(item_counts):

            title = self._str(
                self._p(pb, PATH_WHOLE_CONTENT_DIXY_SKIDKI_NEDELI)[i]
            )

            data = re.findall(r'\d{2}/\d{2}', title)

            if len(data) == 0:
                _start = datetime.today()
                _end = _start + timedelta(days=1)

            elif len(data) == 1:
                _start = datetime.today()
                _end = self._d(data, date_format, add_year=True, now=now)

            else:
                _end = self._d(data, date_format, add_year=True, now=now)
                _start = self._d(data, date_format, add_year=True, now=now)

            # category_i = i * 4 - 1
            # category = self.__str(
            #     self.__p(pb, PATH_CATEGORY_DIXY_SKIDKI_NEDELI)[category_i]
            # )

            price_new = int(
                self._str(
                    self._p(pb, PATH_PRICE_NEW_DIXY_SKIDKI_NEDELI)[i]
                )
            )

            price_old = self._p(pb, PATH_PRICE_OLD_DIXY_SKIDKI_NEDELI)[i]

            if not price_old.isdigit():
                price_old = price_new / 0.9

            yield {
                'name': self._str(
                    self._p(pb, PATH_NAME_DIXY_SKIDKI_NEDELI)[i]
                ),

                'url': '{}{}'.format(
                    BASE_URL,
                    self._str(
                        self._p(pb, PATH_NAME_DIXY_SKIDKI_NEDELI)[i]
                    )
                ),

                'price_new': price_new,
                'price_old': int(price_old),
                'title': title,
                'start': _start,
                'end': _end,
                'promo': ''
            }

    def dixy_week_discount(self):

        page_id, max_page_id = 1, 1

        while page_id <= max_page_id:
            page = '{}{}'.format(BASE_DISCOUNT_URL_DIXY_SKIDKI_NEDELI, page_id)

            try:
                response = requests.get(page)
            except requests.RequestException:
                return 'Cannot reach the page: {}'.format(page)

            pb = html.fromstring(response.text)

            max_page_id = int(self._p(pb, PATH_LAST_PAGE_ID).pop())
            page_active = int(self._p(pb, PATH_ACTIVE_PAGE_NUMBER).pop())

            if page_active == page_id:
                return self.parse_page(pb)

    def combine(self):
        yield from self.dixy_week_discount()
        yield from self.dixy()

    @staticmethod
    def get_actual_promos():

        promos = []

        promo_service = PromoService()

        for e in promo_service.combine():

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
            promo.save()

            promos.append(promo)

        return promos
