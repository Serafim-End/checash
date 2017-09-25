#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import operator
import json
import re
from collections import Counter

from pymystem3 import Mystem
from nltk.corpus import stopwords

class Categorizer:
	def __init__(self, data_path):
		self.lemmer = Mystem()
		self.stop_words = set(stopwords.words('russian'))
		stops = ['что', 'этот', 'где', 'чем', 'кем', 'кому', 'это', 'так', 'вот', 'быть', 'как', 'в', 'к', 'на', 'и']
		self.stop_words.update(stops)
		self.quotes_re = re.compile(u'(\".*?\")|(\'.*?\')')

		self.goods_index = dict()
		with open(data_path, 'r') as f:
			goods_index = json.loads(f.read().strip())
			self.goods_index = { v[0]:v[1] for v in map(lambda s: (self.normalizePhrase(s), goods_index[s]), goods_index.keys()) }

		self.categories_tree = dict()
		for info in self.goods_index.values():
			for i in range(len(info['categs'])):
				self.categories_tree[info['categs'][i]] = info['categs'][i-1] if i != 0 else -1

		'''
		self.l1_index = dict()
		for (phrase, info) in self.goods_index.items():
			if info['l1']:
				if not info['l1'] in self.l1_index:
					self.l1_index[info['l1']] = []
				self.l1_index.append(phrase)
		for categ in self.l1_index:
			self.l1_index['categ'] = sorted(self.l1_index['categ'], key=(lambda phr: self.l1_index[phr]['rating']), reversed=True)
		'''
		self.reverse_index = dict()
		for phrase in self.goods_index.keys():
			for word in phrase.split(' '):
				if not word in self.reverse_index:
					self.reverse_index[word] = []
				self.reverse_index[word].append(phrase)
		pass

	def normalizePhrase(self, phrase):
		phrase = self.quotes_re.sub('', phrase)
		norm = ' '.join( sorted( filter(lambda w: w not in self.stop_words, self.lemmer.lemmatize(phrase)))).strip()
		return norm

	def getPhrasesByIntersection(self, phrase, isNorm=False):
		norm = phrase if isNorm else self.normalizePhrase(phrase)
		result = Counter()
		for word in filter(lambda w: w in self.reverse_index,  norm.split(' ')):
			for phrase in self.reverse_index[word]:
				result[phrase] += 1.0/len(phrase.split(' '))
		return result
	
	def getCategoryParents(self, category):
		result = []
		while category != -1:
			result.append(category)
			category = self.categories_tree[category]
		result.reverse()
		return result

	# 3 уровня категоризации - от широкого к узкому (последний зашифрован)
	def getCategoriesHierarchy(self, phrase):
		norm = self.normalizePhrase(phrase)
		simlist = self.getPhrasesByIntersection(norm, isNorm=True)

#		print "\n".join(simlist)
		# выбираем категорию по наибольшему рейтингу на самом узком уровне
		# рейтинг составляется по сл. алгоритму:
		# 1) берем все фразы из базы категорий, с которыми данная пересекается хотя бы по одному слову
		# 2) рейтинг каждой категории = sum( 1/<rank пер. фразы по данной кат.> * 1/<длина фразы>) по всем пер. фразам из данной кат.
		#
		levels = range(3)
		rating = [dict() for level in levels]
		for cand_phrase in simlist.keys():
			info = self.goods_index[cand_phrase]
			categ = info['categs']
			for level in range(len(rating)):
				categ = info['categs'][level]
				if categ != '':
					if not categ in rating[level]:
						rating[level][categ] = 0.0
					rating[level][categ] += (1.0/float(info['rating']) * simlist[cand_phrase])
		
		# выбираем самую узкую категорию с макс. рейтингом
		for level in reversed(levels):
			if len(rating[level]) > 0:
				categ = max(rating[level].iteritems(), key=operator.itemgetter(1))[0]
				return self.getCategoryParents(categ)
				
		return []
		
	# используем 2-й уровень категоризации (он не зашифрован и не так обширен, как 1-й)
	def getCategory(self, phrase):
		hierarchy = self.getCategoriesHierarchy(phrase)
		if len(hierarchy) == 3:
			return hierarchy[2]
		return hierarchy[-1] if len(hierarchy) else ''

	# близки ли товарные фразы
	def isClose(self, phrase_1, phrase_2):
		norm_1 = self.normalizePhrase(phrase_1)
		norm_2 = self.normalizePhrase(phrase_2)
		cnt_common_words = set(norm_1.split(' ')).intersection(set(norm_2.split(' ')))

		# если > 2 общих слов -- то близки
		if cnt_common_words > 2:
			return True

		hierarchy_1 = self.getCategoriesHierarchy(norm_1, isNorm=True)
		hierarchy_2 = self.getCategoriesHierarchy(norm_2, isNorm=True)
		sim_level = -1
		for level in range(min(len(hierarchy_1), len(hierarchy_2))):
			if hierarchy_1[level] == hierarchy_2[level]:
				sim_level = level
				break
		# если в одной категории на определенном уровне -- то близки
		# можно настраивать точность тут 
		return sim_level == 2 

def test():
	categorizer = Categorizer('dict_goods_categorized')
#	print categorizer.getPhrasesByIntersection(u'подушка')
	phrases = [u'молоко "Домик в Деревне" 2л', u'Подушка "ваше счастье" икеа', u'хлеб черный Дарницкий 1234гр']
	for phr in phrases:
		print categorizer.getCategory(phr)
		print '->'.join(categorizer.getCategoriesHierarchy(phr))
		print ''

	print categorizer.isClose(u'молоко деревенское', u'сметана домашняя')

	return 0

if __name__ == '__main__':
	  sys.exit(test())

