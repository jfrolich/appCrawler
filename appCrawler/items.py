# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class GooglePlayItem(scrapy.Item):
    id = Field()
    url = Field()
    item_name = Field()
    updated = Field()
    author = Field()
    file_size = Field()
    downloads = Field()
    version = Field()
    compatibility = Field()
    content_rating = Field()
    author_link = Field()
    genre = Field()
    price = Field()
    rating_value = Field()
    review_count = Field()
    description = Field()
    iap = Field()
    developer_badge = Field()
    address = Field()
    video_url = Field()
    developer_id = Field()
