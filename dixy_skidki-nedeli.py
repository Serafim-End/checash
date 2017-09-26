# -*- coding: utf-8 -*-
import requests
from lxml import html
import re
import datetime

j = 0
page_id = 1
page_active = 1

while page_id - page_active <= 3:

    page = 'https://dixy.ru/akcii/skidki-nedeli/?PAGEN_1=' + str(page_id)
    response = requests.get(page)
    parsed_body = html.fromstring(response.text)
    page_active = int(parsed_body.xpath('//li[@class="active"]/a[@href="#"]/text()')[0])

    if page_active == page_id:
        l = len(parsed_body.xpath('//div[contains(@class, "elem-badge-cornered")]/text()'))

        for i in range(l):
            title = parsed_body.xpath('//div[contains(@class, "elem-badge-cornered")]/text()')[i].encode('utf-8')
            
            data = re.findall(r'\d{2}/\d{2}', title)
            if len(data) == 0:
                start_date = datetime.datetime.today()
                due_date = datetime.datetime.today() + datetime.timedelta(days=1)
            elif len(data) == 1:
                start_date = datetime.datetime.today()
                due_date = datetime.datetime.strptime(data[0] + '/' + str(datetime.datetime.now().year), "%d/%m/%Y")
            else:
                start_date = datetime.datetime.strptime(data[0] + '/' + str(datetime.datetime.now().year), "%d/%m/%Y")
                due_date = datetime.datetime.strptime(data[1] + '/' + str(datetime.datetime.now().year), "%d/%m/%Y")

            image = parsed_body.xpath('//div[@class="elem-product__image"]/img/@src')[i]
            url = 'https://dixy.ru' + image

            name = parsed_body.xpath('//div[@class="elem-product__image"]/img/@alt')[i].encode('utf-8')
            
            

            j = i * 4 - 1
            category = parsed_body.xpath('//div[@class="product-category"]/text()')[j].encode('utf-8')

            price = parsed_body.xpath('//span[@class="price-discount__integer"]/text()')[i].encode('utf-8')
            price_old = parsed_body.xpath(
                '//div[@class="elem-product__price-container"]/div[@class="just-now"]/text()|//span[@class="price-full__integer"]/text()')[
                i]
            if price_old.isdigit() == False:
                price_old = int(price) / 0.9

            cashback_rub = int(price_old) - int(price)

            print 'title', title
            print 'due_date', due_date
            print 'start_date', start_date
            print 'cashback_rub', cashback_rub
            print 'name', name
            print 'price', price
            print 'url', url
            print 'category', category

            print('############################################')
            print('############################################')

    else:
        break

    page_id += 1
