# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import requests
import json
from urllib import parse
# from scrapy.loader import ItemLoader
from ArticleSpider.items import ArticaleItemLoader
from ArticleSpider.utils import common
from ArticleSpider.items import JobBoleArticleItem
from selenium import webdriver

# from scrapy.xlib.pydispatch import dispatcher

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/news/']



    # custom_settings = {    # 设置知乎自己的setting
    #     "JOBDIR": "job_jinfo/001",
    # }
    #
    # def __init__(self):
    #     self.browser = webdriver.Chrome("C:/Users/孙佩豪/AppData/Local/Google/Chrome/Application/chromedriver.exe")
    #     super(JobboleSpider, self).__init__()   # 变为父类的属性

    handle_httpstatus_list = [404, 301]   # 过滤的请求状态
    def __init__(self):
        self.fail_urls = []


    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed")

        # 提取值 或extract_first("")=extract()[0] 如果list为空 返回默认值""
        # urls = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()
        post_nodes = response.css('#news_list .news_block') # 同上
        for post_node in post_nodes:
            imag_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")  # 图片地址
            if imag_url.startswith("//"):
                imag_url = "https:" + imag_url
            post_url = post_node.css('h2 a::attr(href)').extract_first("")    # 获取url
            # parse拼接url 若post_url带域名 也会自动拼接 callback后续回调函数不要写括号 写括号会直接运行
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": imag_url}, callback=self.parse_detail)  # yield 可以将当下请求下的url 交给Request请求 并且列表页请求继续运行

        # 提取下一页url 交给scrapy进行下载
        # next_url = response.css("div.pager a:last-child::text").extract_first("")

        # next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first("")  # 找到节点内容包含 next的a节点 的href属性 同上
        # yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)  # 回调 调用自己 继续请求下一个列表页

        # next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first("")  # 找到节点内容包含 next的a节点 的href属性 同上
        # if next_url == "Next >":  # 本页出现下一页的标志 则提取下一页的url
        #     next_url = response.css("div.paper a:last-child::attr(href)").extract_first("")
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)



    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.group(1)
            # article_item = JobBoleArticleItem()
            # title = response.css("#news_title a::text").extract_first("")
            # create_date = response.css("#news_info .time::text").extract_first("")
            # match_re1 = re.match(".*?(\d+.*)", create_date)
            # if match_re1:
            #     create_date = match_re1.group(1)
            # content = response.css("#news_content").extract()[0]
            # tag_list = response.css(".news_tags a::text").extract()
            # tags = ",".join(tag_list)
            #
            #
            # # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            # # j_data = json.loads(html.text)
            #
            # article_item['title'] = title
            # article_item['create_date'] = create_date
            # article_item['content'] = content
            # article_item['tags'] = tags
            # if response.meta.get('front_image_url', ''):
            #     article_item['front_image_url'] = [response.meta.get('front_image_url', '')]  # 回调下载图片 必须传入列表
            # else:
            #     article_item['front_image_url'] = []
            #
            # article_item["url"] = response.url
            # print(article_item)

            item_loader = ArticaleItemLoader(item=JobBoleArticleItem(), response=response)
            item_loader.add_css("title", "#news_title a::text")
            item_loader.add_css("content", "#news_content")
            item_loader.add_css("tags", ".news_tags a::text")
            item_loader.add_css("create_date", "#news_info .time::text")
            item_loader.add_value("url", response.url)
            if response.meta.get('front_image_url', ''):
                item_loader.add_value("front_image_url", response.meta.get('front_image_url', ''))

            # article_item = item_loader.load_item()


            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)), meta={"article_item": item_loader, "url": response.url}, callback=self.parse_nums)   # 异步获取ajax数据

            # praise_nums = j_data["DiggCount"]
            # fav_nums = j_data["TotalView"]
            # comment_nums = j_data["CommentCount"]


    def parse_nums(self, response):
        a = response.text
        j_data = json.loads(response.text)
        item_loader = response.meta.get('article_item', '')

        # praise_nums = j_data["DiggCount"]
        # fav_nums = j_data["TotalView"]
        # comment_nums = j_data["CommentCount"]

        item_loader.add_value("fav_nums", j_data["TotalView"])
        item_loader.add_value("praise_nums", j_data["DiggCount"])
        item_loader.add_value("comment_nums", j_data["CommentCount"])
        item_loader.add_value("url_object_id", common.get_md5(response.meta.get('url', '')))
        # article_item['praise_nums'] = praise_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['comment_nums'] = comment_nums
        # article_item['url_object_id'] = common.get_md5(response.meta.get('url', ''))

        article_item = item_loader.load_item()

        yield article_item
