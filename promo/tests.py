
from django.test import TestCase

from .service import PromoService
from .models import Promo


class PromoServiceTestCases(TestCase):

    def setUp(self):
        pass

    def test_actual_promos(self):

        actual_promos = PromoService.get_actual_promos()

        self.assertGreater(
            len(actual_promos), 0,
            msg='no actual promos'
        )

        self.assertIsInstance(
            actual_promos, list,
            msg='promos represents not a list'
        )

        self.assertIsInstance(
            actual_promos.pop(), Promo,
            msg='element of actual_promos is not Promo instance'
        )

