# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from PIL import Image
import requests
from scrapy import Selector
from tools.yundama_requests import YDMHttp
from selenium.webdriver.common.keys import Keys



headers = {
        "HOST": "login.sina.com.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36"
    }

def get_snap(driver):  # 对目标网页进行截屏。这里截的是全屏
    driver.save_screenshot('full_snap.png')
    page_snap_obj=Image.open('full_snap.png')
    return page_snap_obj



# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# browser = webdriver.Chrome('C:/Users/孙佩豪/AppData/Local/Google/Chrome/Application/chromedriver.exe',
#                            chrome_options=chrome_options)
#
# browser.get("https://www.weibo.com/")
# time.sleep(10)

#
#
# browser.find_element_by_xpath('//input[@id="loginname"]').send_keys(Keys.CONTROL + "a")
# browser.find_element_by_xpath('//input[@id="loginname"]').send_keys("15292060685")      # 输入密码
#
# browser.find_element_by_xpath('//input[@type="password"]').send_keys(Keys.CONTROL + "a")
# browser.find_element_by_xpath('//input[@type="password"]').send_keys("qq1362441")      # 输入密码
#
# try:
#     verifycode_image = browser.find_element_by_xpath('//img[@node-type="verifycode_image"]')
# except:
#     verifycode_image = None
#
# if verifycode_image:
#     # image_url = verifycode_image.get_attribute("src")
#     # image_content = requests.get(image_url).content
#     browser.save_screenshot('code.png')
#     location = verifycode_image.location
#     x = location['x']
#     y = location['y']
#     width = verifycode_image.size['width']
#     height = verifycode_image.size['height']
#
#
#     im = Image.open('code.png')
#     im = im.crop((x, y, x + width, y + height))
#     im.save('hehe.png')
#
#     Yundama = YDMHttp("sph116", "qq1362441", 8730, "9f94b142759f9fd86bd0e7a912bbc889")  # 实例化云打码
#     code = Yundama.decode("./hehe.png", 5000, 60)  # 识别
#
#     while True:  # 若识别失败 不停识别 直至成功
#         if code == "":  #
#             code = Yundama.decode("hehe.png", 5000, 60)
#             time.sleep(0.5)
#         else:
#             break
#     browser.find_element_by_xpath('//input[@node-type="verifycode"]').send_keys(code)
#
#
#
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")   # seleium运行js模拟鼠标下拉操作
#     time.sleep(3)

"""
设置chrome_driver不加载图片
"""
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome("C:/Users/孙佩豪/AppData/Local/Google/Chrome/Application/chromedriver.exe", chrome_options=chrome_opt)
# browser.get("https://www.taobao.com")

