# -*- coding: utf-8 -*-

import requests
from lxml import html

url = 'https://dixy.ru/akcii/'
response = requests.get(url)
#print response.content

parsed_body = html.fromstring(response.text)

l = len(parsed_body.xpath('//div[@class="product"]/div/div/img/@alt'))

for i in range(l):
    name = parsed_body.xpath('//div[@class="product"]/div/div/img/@alt')[i]
    photo = parsed_body.xpath('//div[@class="product"]/div/div/img/@src')[i]
    category = parsed_body.xpath('//div[@class="product-info-container"]/div/a/text()')[i]
    fract_new = parsed_body.xpath('//div[@class="fract"]/text()')[i]
    price_new = parsed_body.xpath('//div[@class="price" or @class="price hundred"]/text()')[i]
    price_old = parsed_body.xpath('//div[@class="old-price"]/text()')[i]
    fract_old = parsed_body.xpath('//div[@class="old-price"]/span/text()')[i]
    title = parsed_body.xpath('//div[@class="product-day" or @class="product-title"]//text()')[i]
    promo = parsed_body.xpath('//div[@class="discount  " or @class="value"]/text()')[i]

    print name
    print url + photo
    print category
    print title
    print 'Новая цена (рубли):',  price_new
    print 'Новая цена (копейки): ',  fract_new
    print 'Старая цена (рубли):',price_old
    print 'Старая цена (копейки):',fract_old
    print 'Акция:', promo
    print('############################################')
    print('############################################')
