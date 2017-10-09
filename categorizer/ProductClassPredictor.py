import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

class_predictor = {'Бакалея': 'Бакалея',
 'Барбекю': 'Разное',
 'Вафли, пряники, печенье': 'Хлеб и кондитерские изделия',
 'Готовые блюда и полуфабрикаты': 'Готовые блюда и полуфабрикаты',
 'Детское питание': 'Детское питание',
 'Йогурты': 'Молочные продукты',
 'Консервированные продукты': 'Консервированные продукты',
 'Макароны, паста, крупы': 'Бакалея',
 'Молочные продукты, яйца': 'Молочные продукты',
 'Овощи, фрукты, ягоды': 'Овощи, фрукты, ягоды',
 'Полуфабрикаты, готовые блюда, выпечка': 'Готовые блюда и полуфабрикаты',
 'Птица': 'Птица',
 'Рыба и морепродукты': 'Рыба и морепродукты',
 'Рыбная гастрономия': 'Рыба и морепродукты',
 'Сладости. Мармелад. Нуга. Цукаты': 'Хлеб и кондитерские изделия',
 'Сыры': 'Молочные продукты',
 'Сыры и колбасы': 'Молочные продукты',
 'Хлеб и кондитерские изделия': 'Хлеб и кондитерские изделия',
 'Хлеб, булочки, лепешки': 'Хлеб и кондитерские изделия',
 'Чипсы, сухарики, снеки, попкорн': 'Хлеб и кондитерские изделия'}

class ProductClassPredictor():
    def __init__(self, df_path, ):
        av_df = pd.read_csv(df_path)
        self.vect = TfidfVectorizer()
        self.clf = joblib.load('gridsearch_av_lenta_level2.pkl')
        self.cat = av_df['level2'].astype('category')
        self.vect.fit_transform(av_df['name'])
    def define_class(self, words):
        vector = self.vect.transform(words)
        return list(self.cat.cat.categories[self.clf.predict(vector)])
