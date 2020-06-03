from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 将根目录放入Python搜索目录中

# execute(["scrapy", "crawl", "zhihu"])   # 执行命令
# execute(["scrapy", "crawl", "lagou"])   # 执行命令
# execute(["scrapy", "crawl", "jobbole"])   # 执行命令
execute(["scrapy", "crawl", "zhihu_cookie_pool"])   # 执行命令