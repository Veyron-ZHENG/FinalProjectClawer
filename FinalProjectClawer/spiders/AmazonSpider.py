# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
from FinalProjectClawer.items import AmazonItem

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.cn"]
    start_urls = ["https://www.amazon.cn/product-reviews/B00QJDOLIO/ref=cm_cr_getr_d_paging_summary"]

    def parse(self, response):
        sel = scrapy.Selector(response=response)
        for review in sel.xpath('//div[@data-hook=\"review\"]'):
            num_star_text = review.xpath("div/div//i[@data-hook=\"review-star-rating\"]").extract()[0]
            num_star = re.findall(r'a-star-(\d)',num_star_text)[0]
            color_text = review.xpath("div/div/a[@data-hook=\"format-strip\"]/text()").extract()
            color = color_text[0]
            title = review.xpath('div/div/a[@data-hook=\"review-title\"]/text()').extract()[0]
            review_lines = review.xpath('div/div/span[@data-hook=\"review-body\"]/text()').extract()
            num_agree = review.xpath('div/div/div/span[@data-hook=\"review-voting-widget\"]//span/text()').extract()[0]
            try:
                num = re.findall(r'\d+\,?\d*', num_agree)[0]
            except IndexError:
                num = '0'
            item = AmazonItem()

            body = ''
            for review_line in review_lines:
                body = body+review_line

            item["review_title"] = title.encode("utf-8")
            item["review_body"] = body.encode("utf-8")
            item["help_vote_num"] = num.encode("utf-8")
            item["color"] = color.encode("utf-8")
            item["num_star"] = num_star.encode("utf-8")
            yield item

        try:
            url = sel.xpath('//li[@class=\'a-last\']/a/@href').extract()[0]
            safe = b'/:?='
            url_coded = urllib2.quote(url.encode('utf-8'),safe)
            yield scrapy.Request('https://www.amazon.cn'+url_coded, callback=self.parse)
        except IndexError:
            pass