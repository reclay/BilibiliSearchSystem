# -*- coding: utf-8 -*-


import json
import os
import time
import re

import MySQLdb
import requests
from lxml.html import clean
import lxml.html

import scrapy
import scrapy.cmdline
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from bilibili.items import BilibiliItem

spider_name = "biliSpider"

class BilispiderSpider(scrapy.Spider):
    name = spider_name
    allowed_domains = ["bilibili.com"]
    start_urls = []

    def __init_mysql_connection(self,*args, **kwargs):
        settings = get_project_settings()
        host = settings["MYSQL_CONFIG"]["HOST"]
        user = settings["MYSQL_CONFIG"]["USERNAME"]
        password = settings["MYSQL_CONFIG"]["PASSWORD"]
        db = settings["MYSQL_CONFIG"]["DBNAME"]
        
        self.connection = MySQLdb.connect(host, user, password, db)
        self.cursor = self.connection.cursor()
        self.connection .set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def __del__():
        self.cursor.close()
        self.connection.close()

    def __init_start_urls(self):
        sql = "select url from need_crawl_url where finished_time = 0"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results)>0:
            for i in results:
                self.start_urls.append(i[0])


    def __init__(self, *args, **kwargs):
        self.__init_mysql_connection()
        self.__init_start_urls()
 

    def parse(self, response):
        sel = Selector(response)
        plist_xpath = '//div[@id="plist"]//option/@value'
        plist_sel = sel.xpath(plist_xpath).extract()

        if len(plist_sel)>1:
            for url in plist_sel:
                if url.find("http://www.bilibili.com/")==-1:
                    url = "http://www.bilibili.com/" + url
                yield scrapy.Request(url,callback = self.parse_item)
        else:
            yield self.parse_item(response)

    def parse_item(self,response):

        print "*"*20,response.url
        sel = Selector(response)
        item = BilibiliItem()

        item["url"] = response.url
        item["crawl_time"] = int(time.time())
        item["title"] = ''.join(sel.xpath("//title/text()").extract())
        item["keywords"] = ''.join(sel.xpath('//meta[@name="keywords"]/@content').extract())
        item["description"] = ''.join(sel.xpath('//meta[@name="description"]/@content').extract())
        item["author"] = ''.join(sel.xpath('//meta[@name="author"]/@content').extract())
        item["cover_image"] = ''.join(sel.xpath('//img[@class="cover_image"]/@src').extract())
        item["h_title"] = ''.join(sel.xpath('//h1/@title').extract())
        item["startDate"] = ''.join(sel.xpath('//time[@itemprop="startDate"]/@datetime').extract())
        item["info"] = self.extract_info(sel)
        item["upinfo"] = self.extract_upinfo(sel)
        item["video_info"] = self.extract_video_info(sel)
        item["tag_list"] = self.extract_tag_list(sel)
        #cid aid
        m = re.findall(r"cid=([0-9]+?)\&aid=([0-9]+?)\&",response.body)
        print m
        if len(m) == 1:
            item["cid"] = m[0][0]
            item["aid"] = m[0][1]
            item["comments"] = self.extract_comments(sel,item["aid"])
            item["stats"] = self.extract_stats(sel,item["aid"])

        return item

    def remove_space(self,raw_data):
        data = raw_data.replace("\t",'')
        data = raw_data.replace("\n",'')
        return data
        
    def extract_info(self,sel):
        cleaner = clean.Cleaner(scripts=True,
                            javascript=True,
                            safe_attrs_only=True,
                            safe_attrs=["class","href","src","title",\
                                    "rel","property","typeof"
                                    ],
                            links=False
                  )
        info_xpath = '//div[@class="info"]'
        content = ''.join(sel.xpath(info_xpath).extract())
        clean_data = cleaner.clean_html(lxml.html.fromstring(content))
        data = lxml.html.tostring(clean_data,encoding="utf8")
        return self.remove_space(data)

    def extract_upinfo(self,sel):
        upinfo_xpath = '//div[@class="upinfo"]'
        cleaner = clean.Cleaner(scripts=True,
                            javascript=True,
                            safe_attrs_only=True,
                            safe_attrs=["class","href","src","card",\
                                    "mid","title"
                                    ],
                            links=False
                  )
        content = ''.join(sel.xpath(upinfo_xpath).extract())
        clean_data = cleaner.clean_html(lxml.html.fromstring(content))
        data = lxml.html.tostring(clean_data,encoding="utf8")
        return self.remove_space(data)


    def extract_video_info(self,sel):
        video_info_xpath = '//div[@itemprop="video"]'
        data = ''.join(sel.xpath(video_info_xpath).extract())
        return self.remove_space(data)

    def extract_tag_list(self,sel):
        tag_list_xpath = '//div[@class="v_info"]'
        data = ''.join(sel.xpath(tag_list_xpath).extract())
        return self.remove_space(data)
        

    def extract_comments(self,sel,aid):
        data = []
        url = ("http://api.bilibili.com/x/v2/reply?"
                "jsonp=jsonp&type=1&sort=0&oid={}&pn=1&nohot=1").format(aid)
        content = requests.get(url).content
        data.append(content)
        json_data = json.loads(content)
        try:
            num = json_data["data"]["page"]["num"]
            for pn in range(2,int(num)+1):
                url = ("http://api.bilibili.com/x/v2/reply?"
                "jsonp=jsonp&type=1&sort=0&oid={}&pn={}&nohot=1").format(aid,pn)
                content = requests.get(url).content
                data.append(content)
            return data
        except Exception as e:
            self.logger.critical(e)


    def extract_stats(self,sel,aid):
        settings = get_project_settings()
        url = ("http://api.bilibili.com/archive_stat/stat"
                "?&aid={}&type=jsonp").format(aid)
        content = requests.get(url).content
        return content
   
   

