
import unittest

from .categorizer import Categorizer


class CategorizerTestCases(unittest.TestCase):

    def setUp(self):
        self.categorizer = Categorizer('dict_goods_categorized.json')

        self.names = [
            u'молоко "Домик в Деревне" 2л',
            u'Подушка "ваше счастье" икеа',
            u'хлеб черный Дарницкий 1234гр',
            u'Томаты сливовидные 1 кг',
            u'Сливки Романов луг стерилизованные 10% 200 г',
            u'Картофель мытый упакованный 1 кг',
            u'Огурец длинноплодный 1 шт'
        ]

    def test_exist_result(self):

        for t in self.names:
            self.assertIsNotNone(self.categorizer.get_сategory(t))

    def test_all(self):

        phrases = [u'молоко "Домик в Деревне" 2л', u'Подушка "ваше счастье" икеа',
                   u'хлеб черный Дарницкий 1234гр']

        for phr in phrases:
            print(self.categorizer.get_сategory(phr))
            print()
            print(self.categorizer.get_categories_hierarchy(phr))
            print('')
            print()

        print(
            self.categorizer.isClose(
                u'молоко деревенское', u'сметана домашняя'
            )
        )

        return 0


if __name__ == '__main__':
    unittest.main()
