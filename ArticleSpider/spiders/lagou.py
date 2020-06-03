# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle
import os

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback="parse_job", follow=True),
    )

    def start_requests(self):
        # 去使用selenium模拟登录后拿到cookie交给scrapy的request使用
        # selenium模拟登陆
        # 使用chrome.exe手动启动 进入exe文件路径cmd  输入 chrome --remote-debugging-port=9222

        cookies = {}
        if os.path.exists("./ArticleSpider/cookies/lagou.cookie"):
            cookies = pickle.load(open("./ArticleSpider/cookies/lagou.cookie", "rb"))

        if not cookies:

            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            browser = webdriver.Chrome('C:/Users/孙佩豪/AppData/Local/Google/Chrome/Application/chromedriver.exe',
                                       chrome_options=chrome_options)
            browser.get("https://passport.lagou.com/login/login.html")            # 打开登录页面
            # browser.find_element_by_css_selector(".form_body .input.input input_white HtoC_JS input_warning").send_keys("15292060685")     # 输入帐号
            # browser.find_element_by_css_selector('.form_body input[type="password"]').send_keys("qq1362441")                                       # 输入密码
            # browser.find_element_by_css_selector('div[data-view="passwordLogin"] input.btn_lg').click()                                         # 点击登录
            browser.find_element_by_xpath('//div[@data-view="passwordLogin"]//div[@data-propertyname="username"]/input').send_keys("15292060685")
            browser.find_element_by_xpath('//div[@data-view="passwordLogin"]//div[@data-propertyname="password"]/input').send_keys("qq1362441")
            browser.find_element_by_xpath('//div[@data-view="passwordLogin"]//div[@data-propertyname="submit"]/input').click()


            time.sleep(10)

            cookies = browser.get_cookies()   # 获取登录成功的cookie
            pickle.dump(cookies, open("./ArticleSpider/cookies/lagou.cookie", "wb"))   # 将cookie写入到本地文件

        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, cookies=cookie_dict)


    def parse_job(self, response):
        """
        解析拉勾网的职位
        :param response:
        :return:
        """
        i = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return i

