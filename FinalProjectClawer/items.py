# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AmazonItem(scrapy.Item):
    review_title = scrapy.Field()
    review_body = scrapy.Field()
    help_vote_num = scrapy.Field()
    color = scrapy.Field()
    num_star = scrapy.Field()
