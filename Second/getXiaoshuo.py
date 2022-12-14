import os
from sys import stdout
from typing import Dict, List
from xml import etree

import requests
import re
import time
from bs4 import BeautifulSoup
from tqdm import tqdm, trange


def get_chapter_url_list(book_url: str) -> List[str]:
    """
    根据书籍链接获取全部章节链接列表

    Parameters
    ----------
    book_url : str
        书籍链接

    Returns
    -------
    List[str]
        章节链接列表
    """
    # 匹配章节链接的正则表达式
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
    }
    base_url = 'http://www.xbiquge.la'

    href_regex = "<dd><a href='(.*)' >"
    response = requests.get(book_url, headers=headers)
    response.encoding = 'utf-8'

    chapter_href_list = re.findall(href_regex, response.text)
    return [base_url + href for href in chapter_href_list]


def get_chapter_detail(chapter_url: str) -> Dict[str, str]:
    """
    根据章节链接获取章节信息

    Parameters
    ----------
    chapter_url : str
        章节链接

    Returns
    -------
    Dict[str, str]
        章节链接信息
    """
    # 反复尝试获取,直到有正确的信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
    }

    while 1:
        response = requests.get(chapter_url, headers=headers)
        if '503 Service Temporarily Unavailable' not in response.text:
            break
        else:
            print('漏数据了，3 秒之后继续爬')
            time.sleep(3)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    # 查找正文内容
    content = soup.find(attrs={'id': 'content'}).text
    # 标题
    title = soup.find('h1').text
    return {
        'content': content,
        'title': title,
        'url': chapter_url
    }


def getRescult(book_url, max_chapter_count):
    file_name = "./XiaoShuo/"
    name, autor = get_name_id(book_url)

    # 获取章节列表
    chapter_url_list = get_chapter_url_list(book_url)
    if max_chapter_count!=0:
        chapter_url_list = chapter_url_list[:max_chapter_count]

    # 存储路径
    with open(os.path.join(file_name,name) + ".txt", 'w', encoding='utf-8') as f:
        for index in tqdm(range(len(chapter_url_list)), desc=name + '爬取进度'):
            item = get_chapter_detail(chapter_url_list[index])
            f.write('标题: ' + item['title'] + '\n')
            f.write('原文链接: ' + item['url'] + '\n')
            f.write('正文内容: ' + item['content'] + '\n')

    novel_path = os.path.join(os.getcwd(),"XiaoShuo")
    novel_name = name + ".txt"
    contents = open(os.path.join(novel_path,novel_name), "r").read()
    mylen = len(contents)
    zhanyongsize = os.path.getsize(os.path.join(novel_path,novel_name))
    return [name, autor, mylen, novel_path, novel_name, zhanyongsize]


def get_name_id(book_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
    }
    base_url = 'http://www.xbiquge.la'

    response = requests.get(book_url, headers=headers)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.find(attrs={"property": "og:novel:book_name"})['content']
    autor = soup.find(attrs={"property": "og:novel:author"})['content']

    return name, autor


if __name__ == '__main__':
    # 要采集的最大章节数
    max_chapter_count = 10
    # 书籍链接
    book_url = 'https://www.xbiquge.la/10/10489/'

    getRescult(book_url, 1)
