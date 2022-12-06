# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib3, requests  # python 访问 HTTP 资源的必备库
from pprint import pprint  # 打印出任何python数据结构类和方法的模块


def get_name(telecode):
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9163"
    requests.packages.urllib3.disable_warnings()  # requests模块在访问HTTPS网站时，如果设置移除SSL认证参数“verify=False”，执行代码是会提示“InsecureRequestWarning”警告，再请求页面时加入此段代码可以屏蔽掉警告信息
    r = requests.get(url, verify=False)  # 请求12306网站的所有城市的拼音和代号网页，verify=False参数表示不验证证书
    # result = re.findall(r'([A-Z]+)\|([a-z]+)', r.text)    # 通过正则表达式来匹配车站中文拼音和英文编号对应的数据
    result = re.findall(r"([\u4e00-\u9fa5]+)\|([A-Z]+)", r.text)  # 通过正则表达式来匹配车站中文名和英文编号对应的数据
    stations = dict(result)  # 将获取的数据转成字典
    # print(stations["上海虹桥"])     # 验证用
    """
        请将下面输出的结果保存到stations.py中，并在文件开头添加一行：# coding=gbk
        否则在调用stations.py文件时，会提示报错。
    """
    # print(stations.keys())
    # print(stations.values())
    # print(list(stations.keys())[list(stations.values()).index(telecode)])
    return list(stations.keys())[list(stations.values()).index(telecode)]


def get_telecode(name):
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9163"
    requests.packages.urllib3.disable_warnings()  # requests模块在访问HTTPS网站时，如果设置移除SSL认证参数“verify=False”，执行代码是会提示“InsecureRequestWarning”警告，再请求页面时加入此段代码可以屏蔽掉警告信息
    r = requests.get(url, verify=False)  # 请求12306网站的所有城市的拼音和代号网页，verify=False参数表示不验证证书
    # result = re.findall(r'([A-Z]+)\|([a-z]+)', r.text)    # 通过正则表达式来匹配车站中文拼音和英文编号对应的数据
    result = re.findall(r"([\u4e00-\u9fa5]+)\|([A-Z]+)", r.text)  # 通过正则表达式来匹配车站中文名和英文编号对应的数据
    stations = dict(result)  # 将获取的数据转成字典
    # print(stations["上海虹桥"])     # 验证用
    """
        请将下面输出的结果保存到stations.py中，并在文件开头添加一行：# coding=gbk
        否则在调用stations.py文件时，会提示报错。
    """

    # print(stations.keys())
    # print(stations.values())
    # print(stations[name])
    return stations[name]


