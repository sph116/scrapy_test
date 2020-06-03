 # -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join
from ArticleSpider.utils.common import extract_num
import datetime
from ArticleSpider.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# def add_jobbole(value):
#     return value+"-bobby"

def date_convert(value):
    """
    提取时间
    :param value:
    :return:
    """
    match_re1 = re.match(".*?(\d+.*)", value)
    if match_re1:
        create_date = match_re1.group(1)
        return create_date
    else:
        return '1970-07-01'

class ArticaleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor=MapCompose(add_jobbole),   # 全部元素处理
        # output_processor=TakeFirst()   # 提取列表第一个值
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=Identity()   # 保持原样 为列表
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(separator=",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        """
        返回存储 item的sql和params
        :return:
        """
        insert_sql = """
                            insert into jobbole_article(title, url, url_object_id, front_image_url, front_image_path, praise_nums, comment_nums, fav_nums, tags, content, create_date)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE fav_nums=VALUES(fav_nums)
                        """
        params = (self["title"], self["url"], self["url_object_id"], self["front_image_url"], self["front_image_path"], self["praise_nums"], self["comment_nums"], self["fav_nums"], self["tags"], self["content"], self["create_date"])
        return insert_sql, params

class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        """
        插入知乎question表的sql
        :return:
        """
        insert_sql = """
                    insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num), watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num), 

                                """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))

        comments_num = extract_num("".join(self["comments_num"]))
        watch_user_num = extract_num("".join(self["watch_user_num"][0]))
        if len(self["watch_user_num"]) == 2:
            click_num = extract_num("".join(self["watch_user_num"][1]))
        else:
            click_num = 0

        # click_num = extract_num("".join(self["click_num"]))
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)

        return insert_sql, params

class ZhihuAnswerItem(scrapy.Item):
    # 知乎问题回答的item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        """
        插入知乎question表的sql
        :return:
        """

        insert_sql = """
                    insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, parise_num, comments_num, create_time, update_time, crawl_time)
                    ON DUPLICATE KEY UPDATE content=VALUES(content), content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num), update_time=VALUES(update_time), 
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
        # 主
        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)   # 将int类型转换为datetime类型
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)

        params = (
            self["zhihu_id"],
            self["url"],
            self["question_id"],
            self["author_id"],
            self["content"],
            self["parise_num"],
            self["comments_num"],
            create_time,
            update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),  # 提取出

        )
        return insert_sql, params



