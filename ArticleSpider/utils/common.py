import hashlib
import re

def get_md5(url):
    """
    将传入字符串加密为md5形式
    :param url:
    :return:
    """
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()


def extract_num(text):
    """
    从字符串中提取出数字
    :param text:
    :return:
    """
    match_re1 = re.match(".*?(\d+).*", text)
    if match_re1:
        create_date = match_re1.group(1)
        # print("提取数字", create_date)
        return create_date
    else:
        return 0



if __name__ == "__main__":

    print(get_md5("https://cnblogs.com"))