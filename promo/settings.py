
BASE_URL = 'https://dixy.ru'
BASE_DISCOUNT_URL = '{}{}'.format(BASE_URL, '/akcii')
PATH_WHOLE_CONTENT = '//div[@class="product"]/div/div/img/@alt'
PATH_NAME = '//div[@class="product"]/div/div/img/@alt'
PATH_PHOTO = '//div[@class="product"]/div/div/img/@src'
PATH_CATEGORY = '//div[@class="product-info-container"]/div/a/text()'
PATH_FRACT_NEW = '//div[@class="fract"]/text()'
PATH_PRICE_NEW = '//div[@class="price" or @class="price hundred"]/text()'
PATH_PRICE_OLD = '//div[@class="old-price"]/text()'
PATH_FRACT_OLD = '//div[@class="old-price"]/span/text()'
PATH_TITLE = '//div[@class="product-day" or @class="product-title"]//text()'
PATH_PROMO = '//div[@class="discount  " or @class="value"]/text()'
