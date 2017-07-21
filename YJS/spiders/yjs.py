# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from YJS.helper import md5
import time
from YJS.items import YjsOtherItem,YjsSelfItem
from scrapy.loader import ItemLoader

class YjsSpider(scrapy.Spider):
    name = 'yjs'
    allowed_domains = ['yingjiesheng.com']
    start_urls = ['http://s.yingjiesheng.com/search.php?word=%E5%BC%80%E5%8F%91+-%E6%88%BF%E5%9C%B0%E4%BA%A7+-%E8%AF%BE%E7%A8%8B+-%E5%9F%B9%E7%94%9F+-%E9%94%80%E5%94%AE+%E6%A0%A1%E6%8B%9B&area=0&do=1']

    # 列表页数据获取
    def parse(self, response):

        import re

        """

        1.获取列表url，交给scrapy下载后进行详情解析
        2。获取下一页url交给scrapy进行下载，下载完后交给parse提取url

        """
        # 获取数据部分
        post_part = response.xpath("//ul[contains(@class,'searchResult')]/li")

        for post_node in post_part:
            # 标题
            title_selector = post_node.xpath("div/h3/a")
            title = title_selector.xpath('string(.)').extract_first('')
            # 信息来源
            tag_original = post_node.xpath("div/p/text()").extract_first('')
            tag_deal = tag_original.replace(' ','').replace('\r\n','')
            tag_obj = re.match(".*?\：(.*)",tag_deal)
            if tag_obj:
                tag = tag_obj.group(1)
            else:
                tag = ""
            # 查找标签是否有本站 没有type值为 -1
            type = 1 if tag.find("本站") != -1 else 0
            # 页面链接
            post_url = post_node.xpath("div/h3/a/@href").extract_first()
            # 抓去详情数据
            if type:
                yield Request(url=parse.urljoin(response.url,post_url),meta={"title":title,"tag":tag,"type":type},callback=self.pars_self)
            else:
                yield Request(url=parse.urljoin(response.url,post_url),meta={"title":title,"tag":tag},callback=self.pars_other)

            # 变量初始化
            title_selector = ''
            source_original = ''

        next_url = response.xpath("//div[contains(@class,'page')]/a[text()='下一页']/@href").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    # 其他网站数据详情获取
    def pars_other(self,response):

        # 实例化item
        yjs_other_item = YjsOtherItem()

        type = response.meta.get("type","")

        title = response.meta.get("title","")
        url = response.url
        url_md5 = md5(url)
        tag = response.meta.get("tag","")

        company = response.xpath("//div[contains(@class,'mleft')]/h1/text()").extract_first("")
        post_date = response.xpath("//div[contains(@class,'info clearfix')]/ol/li[text()='发布时间：']/u/text()").extract_first("")
        location = response.xpath("//div[contains(@class,'info clearfix')]/ol/li[text()='工作地点：']/u/text()").extract_first("")
        position_type = response.xpath("//div[contains(@class,'info clearfix')]/ol/li[text()='职位类型：']/u/text()").extract_first("")
        source = response.xpath("//div[contains(@class,'info clearfix')]/ol/li[text()='来源：']/a/text()").extract_first("")
        position = response.xpath("//div[contains(@class,'info clearfix')]/ol/li[text()='职位：']/u/text()").extract_first("")
        major_label = ''

        content_obj = response.xpath("//div[contains(@class,'job')]")
        content = content_obj.xpath("string(.)").extract_first("")

        created_at = int(time.time())

        yjs_other_item['title'] = title
        yjs_other_item['url'] = url
        yjs_other_item['url_md5'] = url_md5
        yjs_other_item['tag'] = tag

        yield yjs_other_item


    # 本站数据详情获取
    def pars_self(self,response):

        import re

        # 实例化item
        yjs_self_item = YjsSelfItem()

        type = response.meta.get("type","")

        title = response.meta.get("title", "")
        url = response.url
        url_md5 = md5(url)
        tag = response.meta.get("tag", "")

        company = response.xpath("//div[contains(@class,'main')]/div[1]/h1/a/text()").extract_first()
        industry = response.xpath("//div[contains(@class,'main')]/div[1]/ul/li[1]/span/text()").extract_first()
        company_size = response.xpath("//div[contains(@class,'main')]/div[1]/ul/li[2]/span/text()").extract_first()
        company_type = response.xpath("//div[contains(@class,'main')]/div[1]/ul/li[3]/span/text()").extract_first()

        position_title_obj = response.xpath("//div[contains(@class,'main')]/div[2]/h2")
        position_title = position_title_obj.xpath("string(.)").extract_first()

        location = response.xpath("//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[1]/span/a/text()").extract_first()
        valid_date = response.xpath("//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[2]/span/text()").extract_first()

        recruit_num_original = response.xpath("//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[3]/span/text()").extract_first()
        recruit_num_regular = re.match("([\d]*).*",recruit_num_original)
        recruit_num = recruit_num_regular.group(1)

        position_type_original = response.xpath("//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[4]/text()").extract_first()
        position_type_regular = re.match("职位性质：(.*)",position_type_original)
        position_type = position_type_regular.group(1)

        position_desc_obj = response.xpath("//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/div[contains(@class,'j_i')]")
        position_desc = position_desc_obj.xpath("string(.)").extract_first()

        company_intro_obj = response.xpath("//div[contains(@class,'main')]/div[4]/p")
        company_intro = company_intro_obj.xpath("string(.)").extract_first()

        company_site = response.xpath("//div[contains(@class,'main')]/div[4]/ul/li/a/text()").extract_first()
        cteated_at = int(time.time())

        yjs_self_item['title'] = title
        yjs_self_item['url'] = url
        yjs_self_item['url_md5'] = url_md5
        yjs_self_item['tag'] = tag

        yield yjs_self_item
