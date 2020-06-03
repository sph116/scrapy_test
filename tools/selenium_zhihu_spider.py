# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from scrapy import Selector

browser = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')

"""
测试
"""
# browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025;12304035:3222910")
# print(browser.page_source)   # 打印页面的html 尽量不要使用selenium自带模块解析数据 使用lxml
#
# t_selector = Selector(text=browser.page_source)
# print(t_selector.css(".tm-promo-price .tm-price::text").extract())
# browser.quit()

browser.get("https://www.zhihu.com/signin")
time.sleep(2)

# browser.find_element_by_class_name("SignFlow-tab").click()

browser.find_element_by_xpath('//div[@class="SignFlow-tab"]').click()

time.sleep(2)

browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("18782902568")
browser.find_element_by_css_selector(".SignFlow-password input").send_keys("admin1234")

browser.find_element_by_xpath('//button[@class="Button SignFlow-submitButton Button--primary Button--blue"]').click()  # 点击登录