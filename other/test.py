# import pymysql
# import redis
# import requests
# from lxml import etree
# import time
import time

from lxml import etree
from pandas import Series, DataFrame
import pandas as pd
import re
import asyncio
import aiohttp
#
# import random
#
# import requests
# from lxml import etree
#
# PASSWD = 'uniccc2019'
# HOST = '221.214.181.70'
#
# def get_cookies(db=14):
#     """
#     获取普通cookie
#     :param db:
#     :return:
#     """
#     connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
#     keys = connect.keys()
#     key = random.choice(keys)
#     value = connect.zrange(key, 0, -1)
#     cookies = value[0].decode('utf-8')[:-1] if value else ''
#     return cookies
#
# INFO = {
#     'host': '192.168.1.5',
#     'user': 'root',
#     'password': 'root',
#     'db': 'tyc_dev',
#     'charset': 'utf8'
# }
#
# connection = pymysql.connect(**INFO)
# cursor = connection.cursor()
# cursor.execute('select prov_short_name from das_tm_base_city_info')
# result = cursor.fetchall()
# for i in result:
#     print(i[0])
#     headers = {
#         'Cookie': get_cookies()
#     }
#     resp = requests.get(f'https://www.tianyancha.com/search?base={i[0]}', headers=headers)
#     code = etree.HTML(resp.text)
#     a = code.xpath('//div[@class="filter-scope -expand"]/div[@class="scope-box"]/a/@href')
#     name = code.xpath('//div[@class="filter-scope -expand"]/div[@class="scope-box"]/a/text()')
#     if a:
#         lis = [url.split('=')[-1] for url in a]
#         info = list(zip(name, lis))
#         for city_name, short_name in info:
#             cursor.execute(f'select id from das_tm_base_region_info where region_name = "{city_name}"')
#             data = cursor.fetchone()
#             if not data:
#                 print(city_name, short_name, i[0])
#                 cursor.execute(f'insert into das_tm_base_region_info (region_code, region_name) value ("{short_name}", "{city_name}")')
#                 connection.commit()
#     time.sleep(1.5)
#
#
import gevent
from gevent import monkey
# monkey.patch_all()

import requests


data_li = []
class Spider():
    def __init__(self, url):
        self.url_list = [url for i in range(512)]

    async def parse_detail(self, li):
        title = ''.join(li.xpath('.//p[@class="product-tit"]/a[1]/@title'))
        print(title)

    async def parse(self, url, session):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        async with session.get(url, headers=headers) as resp:
            html = etree.HTML(await resp.text())
            lis = html.xpath('//ul[@class="list"]/li')
            await asyncio.gather(*[self.parse_detail(li) for li in lis])

    async def run(self):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.parse(url, session) for url in self.url_list])

class SpiderInfo():
    def __init__(self, url):
        self.url_list = [url for i in range(512)]

    def parse_detail(self, li):
        title = ''.join(li.xpath('.//p[@class="product-tit"]/a[1]/@title'))
        print(title)

    def parse(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        html = etree.HTML(resp.text)
        lis = html.xpath('//ul[@class="list"]/li')
        for i in lis:
            self.parse_detail(i)

    def run(self):
        spawn_list = []
        for url in self.url_list:
            spawn_list.append(gevent.spawn(self.parse, url))

        gevent.joinall(spawn_list)


class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._registry = {
            'name': name,
            'age': age
        }

    def __getattribute__(self, item):
        # 注意此处不要再访问属性，如self.__dict__[item]
        # 因为self.__dict__依然会被__getattribute__拦截，这样就会陷入死循环
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        print("don't have the attribute ", item)
        return False

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        # print(123)

# print(a.cs)      #这里会打印 don't have the attribute cs 以及 False
# a.cs = '测试'     #这里设置该属性值为'测试'
# print(a.cs)      #这里将打印出'测试'


if __name__ == '__main__':
    start_time = time.time()
    # spider = Spider('https://www.zhaoshang.net/yuanqu/list/')
    # spider2 = SpiderInfo('https://www.zhaoshang.net/yuanqu/list/')
    # spider2.run()
    # asyncio.run(spider.run())
    a = Person('p1', 20)
    # print(a.cs)
    a.cs = 'a'
    print(a.cs)
    end_time = time.time()
    print(f'运行时间 - - :', end_time - start_time)
