# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import time
from YJS.items import YjsItem, YjsOtherItem, YjsSelfItem


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
            # 抓取详情数据
            if title != "":
                if type:
                    yield Request(url=parse.urljoin(response.url,post_url),meta={"title":title, "tag":tag, "type":type},callback=self.pars_self)
                else:
                    yield Request(url=parse.urljoin(response.url,post_url),meta={"title":title, "tag":tag, "type":type},callback=self.pars_other)

            # 变量初始化
            title_selector = ''
            source_original = ''

        next_url = response.xpath("//div[contains(@class,'page')]/a[text()='下一页']/@href").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    # 其他网站数据详情获取
    def pars_other(self,response):

        item_loader = YjsItem(item=YjsOtherItem(), response=response)
        item_loader.add_value("type", response.meta.get("type", ""))
        item_loader.add_value("title", response.meta.get("title", ""))
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_md5", response.url)
        item_loader.add_value("tag", response.meta.get("tag", ""))
        item_loader.add_xpath("company", "//div[contains(@class,'mleft')]/h1/text()")
        item_loader.add_xpath("post_date", "//div[contains(@class,'info clearfix')]/ol/li[text()='发布时间：']/u/text()")
        item_loader.add_xpath("position_type", "//div[contains(@class,'info clearfix')]/ol/li[text()='职位类型：']/u/text()")
        item_loader.add_xpath("source", "//div[contains(@class,'info clearfix')]/ol/li[text()='来源：']/a/text()")
        item_loader.add_xpath("position", "//div[contains(@class,'info clearfix')]/ol/li[text()='职位：']/u/text()")
        item_loader.add_value("major_label", "")
        item_loader.add_value("content", response.xpath("//div[contains(@class,'job')]").xpath("string(.)").extract_first(""))
        item_loader.add_value("created_at", int(time.time()))

        yjs_other_item = item_loader.load_item()
        yield yjs_other_item


    # 本站数据详情获取
    def pars_self(self,response):

        item_loader = YjsItem(item=YjsSelfItem(), response=response)
        item_loader.add_value("type", response.meta.get("type", ""))
        item_loader.add_value("title", response.meta.get("title", ""))
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_md5", response.url)
        item_loader.add_value("tag", response.meta.get("tag", ""))
        item_loader.add_xpath("company", "//div[contains(@class,'main')]/div[1]/h1/a/text()")
        item_loader.add_xpath("industry", "//div[contains(@class,'main')]/div[1]/ul/li[1]/span/text()")
        item_loader.add_xpath("company_size", "//div[contains(@class,'main')]/div[1]/ul/li[2]/span/text()")
        item_loader.add_xpath("company_type", "//div[contains(@class,'main')]/div[1]/ul/li[3]/span/text()")
        item_loader.add_value("position_title", response.xpath("//div[contains(@class,'main')]/div[2]/h2").xpath("string(.)").extract_first())
        item_loader.add_xpath("location", "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[1]/span/a/text()")
        item_loader.add_xpath("valid_date", "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[2]/span/text()")
        item_loader.add_xpath("recruit_num", "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[3]/span/text()")
        item_loader.add_xpath("position_type", "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[4]/text()")
        item_loader.add_value("position_desc", response.xpath("//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/div[contains(@class,'j_i')]").xpath("string(.)").extract_first())
        item_loader.add_value("company_intro", response.xpath("//div[contains(@class,'main')]/div[4]/p").xpath("string(.)").extract_first())
        item_loader.add_xpath("company_site", "//div[contains(@class,'main')]/div[4]/ul/li/a/text()")
        item_loader.add_value("created_at", int(time.time()))

        yjs_self_item = item_loader.load_item()
        yield yjs_self_item
