# -*- coding: utf-8 -*-
import scrapy
import redis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time
import re
from mouse import move, click
from selenium.webdriver.common.keys import Keys
import base64
from zheye import zheye
from tools.yundama_requests import YDMHttp
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem
import json
import datetime
# from ArticleSpider.settings import user_agent_List
import random


class ZhihuCookiePoolSpider(scrapy.Spider):
    name = 'zhihu_cookie_pool'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # 提取完问题信息后 使用起始url提取回答信息  包含三个参数 依次 问题id 返回回答数量 起始序号
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&platform=desktop&sort_by=default"

    # random_index = random.randint(0, len(user_agent_List)-1)  # 提取出随机的UA
    # random_agent = user_agent_List[random_index]

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {    # 设置知乎自己的setting
        "COOKIES_ENABLED": True
    }

    def __init__(self, name=None, **kwargs):
        self.redis_cli = redis.Redis("127.0.0.1", port=6379, password="123456")
        super().__init__(name, **kwargs)    # 调用父类init



    def parse(self, response):
        """
        解析问题列表 提取每个问题url 及id
        :param response:
        :return:
        """
        pass


    def parse_question(self, response):

        """
        进入chrome.exe执行路径 手动启动chrome chrome.exe --remote-debugging-port=9222
        解析每个问题详情页数据 提取具体question item
        :param response:
        :return:
        """
        pass

    def parse_answer(self, response):
        """
        解析请求到的回答数据
        :param response:
        :return:
        """




    def start_requests(self):

        for url in self.start_urls:
            # 从redis中随机获取一个cookie给request
            cookie_str = self.redis_cli.srandmember("zhihu:cookies")
            cookie_dict = json.loads(cookie_str)
            yield scrapy.Request(url, cookies=cookie_dict, dont_filter=True)







