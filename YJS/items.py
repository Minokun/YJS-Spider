# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from YJS.helper import md5
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose , Compose


def GetMd5(value):
    return md5(value)


# 他妹的，这人数居然还有"多人"这个写法！
def GetRecruitNum(value):
    num_obj = re.match("([\d]*).*", value)
    if num_obj:
        return str(num_obj.group(1))
    else:
        num_obj = re.match("([\u4e00-\u9fa5]*).*",value)
        return num_obj.group(1)


def GetPositionType(value):
    position_type_obj = re.match("职位性质：(.*)", value)
    position_type = position_type_obj.group(1) if position_type_obj else "未知"
    return position_type


def RemoveBlankCharacter(value):
    return value.replace("\r\n","").replace("\t","")


class YjsItemLoader(ItemLoader):
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
    position_desc = scrapy.Field(
        input_processor=MapCompose(RemoveBlankCharacter),
    )
    company_intro = scrapy.Field(
        input_processor=MapCompose(RemoveBlankCharacter),
    )
    company_site = scrapy.Field()
    created_at = scrapy.Field()
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
    position_title = scrapy.Field()
    position_type = scrapy.Field()
    source = scrapy.Field()
    major_label = scrapy.Field()
    content = scrapy.Field(
        input_processor = MapCompose(RemoveBlankCharacter),
    )
    created_at = scrapy.Field()