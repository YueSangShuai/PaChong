import os
import time
import requests
from selenium import webdriver
from lxml import etree
from tqdm import tqdm, trange


def getChapterUrl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }
    part_url = "http://ac.qq.com"
    res = requests.get(url, headers=headers)
    html = res.content.decode()
    el = etree.HTML(html)
    li_list = el.xpath('//*[@id="chapter"]/div[2]/ol[1]/li')

    rescult_title = []

    span_list = []
    for li in li_list:
        for p in li.xpath("./p"):
            for span in p.xpath("./span[@class='works-chapter-item']"):
                item = {}
                list_title = span.xpath("./a/@title")[0].replace(' ', '').split('：')
                rescult_title.append(list_title)
                span_list.append(part_url + span.xpath("./a/@href")[0])
    return rescult_title, span_list


def getChapterFile(url, path1, path2):
    # path = os.path.join(path)
    # 漫画名称目录
    path = os.path.join(path1)
    if not os.path.exists(path):
        os.mkdir(path)
    # 章节目录
    if not os.path.exists(path2):
        os.mkdir(path2)
    chrome = webdriver.Chrome()
    chrome.get(url)
    time.sleep(4)
    imgs = chrome.find_elements_by_xpath("//div[@id='mainView']/ul[@id='comicContain']//img")
    data = path2.split('/')
    for i in tqdm(range(len(imgs)), desc=data[2] + '爬取进度'):
        js = "document.getElementById('mainView').scrollTop=" + str((i) * 1280)
        chrome.execute_script(js)
        with open(path2 + '/' + str(i) + '.png', 'wb') as f:
            f.write(requests.get(imgs[i].get_attribute("src")).content)
    chrome.close()


def getRescult(url1, maxsize):
    temp1, temp2 = getChapterUrl(url1)
    if maxsize != 0:
        temp1 = temp1[:maxsize]
        temp2 = temp2[:maxsize]

    for i in range(len(temp1)):
        temp = "manhua/" + temp1[i][0] + "/" + temp1[i][1]
        getChapterFile(temp2[i], "manhua/" + temp1[i][0], temp)


if __name__ == '__main__':
    getRescult('https://ac.qq.com/Comic/comicInfo/id/649980', 10)
