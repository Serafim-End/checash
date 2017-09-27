
import operator
import json
import ssl
import re

from collections import Counter

from pymystem3 import Mystem

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords


class Categorizer(object):
    def __init__(self, data_path):
        self.lemmer = Mystem()

        self.stop_words = set(stopwords.words('russian'))
        stops = ['что', 'этот', 'где', 'чем', 'кем', 'кому',
                 'это', 'так', 'вот', 'быть', 'как', 'в', 'к', 'на', 'и']

        self.stop_words.update(stops)
        self.quotes_re = re.compile(u'(\".*?\")|(\'.*?\')')

        self.goods_index = {}
        with open(data_path, 'r', encoding='utf-8') as f:
            goods_index = json.load(f)

            self.goods_index = {
                self.normalize_phrase(k): v for k, v in goods_index.items()
            }

        self.categories_tree = {}
        for info in self.goods_index.values():
            for i in range(len(info['categs'])):
                self.categories_tree[info['categs'][i]] = (
                    info['categs'][i - 1] if i != 0 else -1
                )

        self.reverse_index = {}
        for phrase in self.goods_index.keys():
            for word in phrase.split(' '):
                if word not in self.reverse_index:
                    self.reverse_index[word] = []
                self.reverse_index[word].append(phrase)

    def normalize_phrase(self, phrase):
        phrase = self.quotes_re.sub('', phrase)
        norm = ' '.join(
            sorted(
                filter(lambda w: w not in self.stop_words,
                       self.lemmer.lemmatize(phrase))
            )
        ).strip('-+ \n')

        return norm

    def get_phrases_by_intersection(self, phrase, is_norm=False):
        norm = phrase if is_norm else self.normalize_phrase(phrase)

        result = Counter()
        for word in filter(lambda w: w in self.reverse_index, norm.split(' ')):
            for phrase in self.reverse_index[word]:
                result[phrase] += 1. / len(phrase.split(' '))
        return result

    def get_category_parents(self, category):
        result = []
        while category != -1:
            result.append(category)
            category = self.categories_tree[category]
        result.reverse()
        return result

    def get_categories_hierarchy(self, phrase):
        """
         3 уровня категоризации - от широкого к узкому (последний зашифрован)
        :param phrase:
        :return:
        """
        norm = self.normalize_phrase(phrase)
        sim_list = self.get_phrases_by_intersection(norm, is_norm=True)

        # print("\n".join(sim_list))
        # выбираем категорию по наибольшему рейтингу на самом узком уровне
        # рейтинг составляется по сл. алгоритму:
        # 1) берем все фразы из базы категорий,
        #  с которыми данная пересекается хотя бы по одному слову
        # 2) рейтинг каждой категории = sum(
        #    1/<rank пер. фразы по данной кат.> * 1/<длина фразы>
        # ) по всем пер. фразам из данной кат.

        levels = range(3)
        rating = [{} for _ in levels]
        for cand_phrase in sim_list.keys():
            info = self.goods_index[cand_phrase]
            for level in range(len(rating)):
                categ = info['categs'][level]
                if categ:
                    if categ not in rating[level]:
                        rating[level][categ] = 0.0
                    rating[level][categ] += (
                        1.0 / float(info['rating']) * sim_list[cand_phrase]
                    )

        # выбираем самую узкую категорию с макс. рейтингом
        for level in reversed(levels):
            if len(rating[level]) > 0:
                categ = max(rating[level].items(),
                            key=operator.itemgetter(1))[0]

                return self.get_category_parents(categ)

        return []

    def get_сategory(self, phrase):
        """
        используем 2-й уровень категоризации
         (он не зашифрован и не так обширен, как 1-й)

        :param phrase:
        :return:
        """
        hierarchy = self.get_categories_hierarchy(phrase)
        if len(hierarchy) == 3:
            return hierarchy[2]
        return hierarchy[-1] if len(hierarchy) else ''

    # близки ли товарные фразы
    def isClose(self, phrase_1, phrase_2):
        norm_1 = self.normalize_phrase(phrase_1)
        norm_2 = self.normalize_phrase(phrase_2)
        cnt_common_words = len(set(norm_1.split(' ')).intersection(
            set(norm_2.split(' '))))

        # если > 2 общих слов -- то близки
        if cnt_common_words > 2:
            return True

        hierarchy_1 = self.get_categories_hierarchy(norm_1)
        hierarchy_2 = self.get_categories_hierarchy(norm_2)
        sim_level = -1
        for level in range(min(len(hierarchy_1), len(hierarchy_2))):
            if hierarchy_1[level] == hierarchy_2[level]:
                sim_level = level
                break

        # если в одной категории на определенном уровне -- то близки
        # можно настраивать точность тут
        return sim_level == 2


def test():
    categorizer = Categorizer('dict_goods_categorized.json')
    # print categorizer.getPhrasesByIntersection(u'подушка')
    phrases = [u'молоко "Домик в Деревне" 2л', u'Подушка "ваше счастье" икеа',
               u'хлеб черный Дарницкий 1234гр']
    for phr in phrases:
        print(categorizer.get_сategory(phr))
        print('->'.join(categorizer.get_categories_hierarchy(phr)))
        print('')

    print(categorizer.isClose(u'молоко деревенское', u'сметана домашняя'))

    return 0


if __name__ == '__main__':
    test()
