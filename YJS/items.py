# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from YJS.helper import md5
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def GetMd5(value):
    return md5(value)


def GetRecruitNum(value):
    num_obj = re.match("([\d]*).*", value)
    num = num_obj.group(1) if num_obj else 0
    return num


def GetPositionType(value):
    position_type_obj = re.match("职位性质：(.*)", value)
    position_type = position_type_obj.group(1) if position_type_obj else "未知"
    return position_type


class YjsItem(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class YjsSelfItem(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field(
        input_processor = MapCompose(GetMd5),
    )
    title = scrapy.Field()
    tag = scrapy.Field()
    company = scrapy.Field()
    industry = scrapy.Field()
    company_size = scrapy.Field()
    company_type = scrapy.Field()
    position_title = scrapy.Field()
    location = scrapy.Field()
    recruit_num = scrapy.Field(
        input_processor = MapCompose(GetRecruitNum),
    )
    position_type = scrapy.Field(
        input_processor = MapCompose(GetPositionType),
    )
    position_desc = scrapy.Field()
    company_intro = scrapy.Field()
    company_site = scrapy.Field()
    create_at = scrapy.Field()
    valid_date = scrapy.Field()


class YjsOtherItem(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field(
        input_processor = MapCompose(GetMd5),
    )
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