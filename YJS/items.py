# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YjsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class YjsSelfItem(scrapy.Item):
    url = scrapy.Field()
    url_md5 = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field()
    company = scrapy.Field()
    industry = scrapy.Field()
    company_size = scrapy.Field()
    company_type = scrapy.Field()
    position_title = scrapy.Field()
    location = scrapy.Field()
    recruit_num = scrapy.Field()
    position_type = scrapy.Field()
    position_desc = scrapy.Field()
    company_intro = scrapy.Field()
    company_site = scrapy.Field()
    create_at = scrapy.Field()
    valid_date = scrapy.Field()

class YjsOtherItem(scrapy.Item):
    url = scrapy.Field()
    url_md5 = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field()
    company = scrapy.Field()
    post_date = scrapy.Field()
    location = scrapy.Field()
    position_type = scrapy.Field()
    source = scrapy.Field()
    major_label = scrapy.Field()
    content = scrapy.Field()
    created_at = scrapy.Field()