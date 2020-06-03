# -*- coding: utf-8 -*-
import scrapy
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


class JobboleSpider(scrapy.Spider):
    name = 'zhihu'
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


    def parse(self, response):
        """
        解析问题列表 提取每个问题url 及id
        :param response:
        :return:
        """
        # all_urls = response.css("a::attr(href)").extract()
        all_urls = response.xpath('//div[@class="Card TopstoryItem TopstoryItem-isRecommend"]//a/@href').extract()    # 提取页面中所有的页面url
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]    # 拼接知乎的域名
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)  # 提取问题url 和 问题id的正则
            if match_obj:
                request_url = match_obj.group(1)           # 问题url
                # question_id = match_obj.group(2)           # 问题id
                yield scrapy.Request(request_url, callback=self.parse_question)  # 回调下载器 请求url
                # break
            else:
                pass
                yield scrapy.Request(url, callback=self.parse)     # 若未能解析到数据 重新请求解析

    def parse_question(self, response):

        """
        进入chrome.exe执行路径 手动启动chrome chrome.exe --remote-debugging-port=9222
        解析每个问题详情页数据 提取具体question item
        :param response:
        :return:
        """
        if "QuestionHeader-title" in response.text:   # 新版本页面的处理方式
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)  # 提取问题url 和 问题id的正则
            if match_obj:
                question_id = int(match_obj.group(2))  # 问题id
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)    # 实例化itemloader
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".ContentItem-actions button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")


            question_item = item_loader.load_item()
        else:     # 旧版页面的处理方式 已取消
            pass
        # question_url = self.start_answer_url.format(question_id, 20, 0)
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), callback=self.parse_answer)
        yield question_item   # 异步存储问题数据

    def parse_answer(self, response):
        """
        解析请求到的回答数据
        :param response:
        :return:
        """
        ans_json = json.loads(response.text)    # 解析返回数据
        is_end = ans_json["paging"]["is_end"]   # 是否是最后一页
        totals_answer = ans_json["paging"]["totals"]     # 所有的回答数量
        next_url = ans_json["paging"]["next"]     # 回答信息的下一页url

        # 提取回答的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None   # 可能出现匿名用户
            answer_item["content"] = answer["content"] if "content" in answer else None               # 如果不出现
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()      # 当前时间

            yield answer_item   # 异步存储数据

        if not is_end:   # 如果不是最后一页
            yield scrapy.Request(next_url, callback=self.parse_answer)  # 进行下一页回答的请求



    def start_requests(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        browser = webdriver.Chrome('C:/Users/孙佩豪/AppData/Local/Google/Chrome/Application/chromedriver.exe',
                                   chrome_options=chrome_options)
        try:
            browser.maximize_window()   # 最大化窗口
        except:  # 已最大化的情况 代码会出错 捕获错误
            pass

        browser.get('https://www.zhihu.com/signin')    # 打开知乎登录页面
        time.sleep(2)
        # browser.find_element_by_xpath('//div[@class="SignFlow-tabs"]/div[2]').click()    # 点击帐号密码登录


        login_success = False
        try:
            notify_ele = browser.find_element_by_xpath('//div[@class="Popover PushNotifications AppHeader-notifications"]')  # 是否登录成功
            login_success = True
        except:
            pass

        if not login_success:
            move(914, 329)  # 点击 帐号密码登录
            click()
            time.sleep(2)
            browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")     # 全选 然后输入账户密码
            browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("15292060685")
            browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
            browser.find_element_by_css_selector(".SignFlow-password input").send_keys("qq1362441")
            move(955, 566)
            click()
            click()
        # browser.find_element_by_xpath('//button[@class="Button SignFlow-submitButton Button--primary Button--blue"]').click()  # 点击登录按钮
        login_success = False


        while not login_success:
            try:
                time.sleep(1)
                notify_ele = browser.find_element_by_xpath('//div[@class="Popover PushNotifications AppHeader-notifications"]')  # 是否登录成功
                login_success = True
            except:
                pass

            try:
                english_captcha_element = browser.find_element_by_class_name("Captcha-englishImg")   # 是否出现英文验证码
            except:
                english_captcha_element = None

            try:
                chinese_captcha_element = browser.find_element_by_class_name("Captcha-chineseImg")   # 是否出现中文验证码
            except:
                chinese_captcha_element = None

            if chinese_captcha_element:  # 如果产生中文验证码
                time.sleep(1)
                ele_position = chinese_captcha_element.location   # 获取节点坐标
                x_relative = ele_position["x"]                    # x坐标
                y_relative = ele_position["y"]                    # y坐标

                browser_navigation_panel_height = browser.execute_script('return window.outerHeight - window.innerHeight;')   # 浏览器上栏高度
                browser_navigation_panel_height = 70

                time.sleep(3)
                base64_text = chinese_captcha_element.get_attribute("src")   # 提取中文验证码节点的arc属性
                code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")   # 消除图片bs64编码中的无用符号
                fh = open("yzm_cn.jpeg", "wb")   # 保存文件
                fh.write(base64.b64decode(code))
                fh.close()

                z = zheye()
                positions = z.Recognize('yzm_cn.jpeg')  # 使用者也 提取倒立文字坐标

                last_position = []
                if len(positions) == 2:
                    if positions[0][0] > positions[1][0]:  # 按照顺序排列倒立文字坐标
                        last_position.append([positions[1][0], positions[1][1]])
                        last_position.append([positions[0][0], positions[0][1]])
                    else:
                        last_position.append([positions[0][0], positions[0][1]])
                        last_position.append([positions[1][0], positions[1][0]])

                if len(positions) == 2:
                    first_position = [int(last_position[0][1] / 2) + x_relative, int(last_position[0][0] / 2) + y_relative+browser_navigation_panel_height]   # 实际页面中 倒立文字图片为正常图片缩放的一倍 所有坐标需要除2取整 来获得可以在页面中使用的坐标
                    second_position = [int(last_position[1][1] / 2) + x_relative, int(last_position[1][0] / 2) + y_relative+browser_navigation_panel_height]


                    move(first_position[0], first_position[1])   # 坐标 起始点x坐标+倒立文字x坐标   起始点y坐标+浏览器地址栏高度+倒立文字y坐标
                    click()

                    move(second_position[0], second_position[1])
                    click()

                else:  # 如果只有一个倒立文字
                    last_position.append([positions[0][1], positions[0][1]])
                    first_position = [int(last_position[0][1] / 2) + x_relative, int(last_position[0][0] / 2) + browser_navigation_panel_height + y_relative]
                    time.sleep(5)
                    move(first_position[0], first_position[1])
                    time.sleep(5)
                    click()

                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")  # 全选 然后输入账户密码
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("15292060685")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys("qq1362441")
                move(954, 619)
                click()


            if english_captcha_element:  # 如果产生英文验证码
                time.sleep(1)
                base64_text = english_captcha_element.get_attribute("src")
                code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")   # 消除图片bs64编码中的无用符号
                fh = open("yzm_en.jpeg", "wb")   # 保存文件
                fh.write(base64.b64decode(code))
                fh.close()

                Yundama = YDMHttp("sph116", "qq1362441", 8730, "9f94b142759f9fd86bd0e7a912bbc889")   # 实例化云打码
                code = Yundama.decode("yzm_en.jpeg", 5000, 60)   # 识别
                while True:   # 若识别失败 不停识别 直至成功
                    if code == "":   #
                        code = Yundama.decode("yzm_en.jpeg", 5000, 60)
                        time.sleep(0.5)
                    else:
                        break



                browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/label/input').send_keys(Keys.CONTROL + "a")   # 找到英文验证码位置
                browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/label/input').send_keys(code)
                move(956, 600)
                click()

            time.sleep(5)

            try:
                # notify_element = browser.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")   # 查看是否出现 登录成功的节点
                # login_success = True

                Cookies = browser.get_cookies()       # 获取登录成功的cookie
                print(Cookies)
                cookie_dict = {}
                import pickle
                for cookie in Cookies:
                    # 写入文件
                    # 此处大家修改一下自己文件的所在路径
                    f = open('./ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')   # 存储cookie进入本地
                    pickle.dump(cookie, f)
                    f.close()
                    cookie_dict[cookie['name']] = cookie['value']
                # browser.close()   # 暂时不关闭
                return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]    # 回调 进入解析
            except:
                pass
        print("======知乎登录成功=========")





    # def start_requests(self):    # 为了可以在scrapy中 使用seleium 需要重写Spider.start_requests方法
    #
    #     # chrome_driver被服务器识别
    #     #1. 下载chrome60 chrome_driver被服务器识别2.33
    #     #2. 手动启动chrome 再用selenium调用
    #
    #     # 进入chrome启动路径 chrome.exe --remote-debugging-port=9222
    #     # 浏览器输入 http://127.0.0.1:9222/json 确认已启动服务
    #
    #     cookies = pickle.load(open("./cookies/zhihu.cookie", "rb"))
    #     cookie_dict = {}
    #     for cookie in cookies:
    #         cookie_dict[cookie["name"]] = cookie["value"]
    #     return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]  # dont_filter 是否不过滤/去重
    #
    #     # from selenium.webdriver.chrome.options import Options
    #     # from selenium.webdriver.common.keys import Keys
    #     # chrome_options = Options()
    #     # chrome_options.add_argument("--disable-extensions")
    #     # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #     # browser = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',
    #     #                            chrome_options=chrome_options)
    #
    #     # browser.get('https://www.zhihu.com/signin')    # 打开知乎登录页面
    #     # browser.find_element_by_xpath('//div[@class="SignFlow-tab"]').click()    # 点击帐号密码登录
    #     #
    #     # time.sleep(2)
    #     #
    #     # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")     # 全选 然后输入账户密码
    #     # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("18782902568")
    #     # browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
    #     # browser.find_element_by_css_selector(".SignFlow-password input").send_keys("admin1234")
    #     #
    #     # time.sleep(10)
    #     # move(715, 503)
    #     # click()
    #     # browser.find_element_by_xpath('//button[@class="Button SignFlow-submitButton Button--primary Button--blue"]').click()  # 点击登录按钮
    #
    #     # browser.get('https://www.zhihu.com/')
    #     # cookies = browser.get_cookies()   # 拿到登录后的所有cookie
    #     #
    #     # pickle.dump(cookies, open("./cookies/zhihu.cookie", "wb"))
    #     # cookie_dict = {}
    #     # for cookie in cookies:
    #     #     cookie_dict[cookie["name"]] = cookie["value"]
    #     #
    #     # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]   # dont_filter 是否不过滤/去重
    #
