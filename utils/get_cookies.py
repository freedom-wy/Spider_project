import redis
import random

import requests
from lxml import etree

PASSWD = 'uniccc2019'
HOST = '221.214.181.70'

def get_cookies(db=14):
    """
    获取普通cookie
    :param db:
    :return:
    """
    connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
    keys = connect.keys()
    key = random.choice(keys)
    value = connect.zrange(key, 0, -1)
    cookies = value[0].decode('utf-8')[:-1] if value else ''
    return cookies

def get_cookies_and_key(db=14):
    """
    获取cookie和手机号
    :param db:
    :return:
    """
    connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
    keys = connect.keys()
    key = random.choice(keys)
    key = key.decode('utf-8') if key else ''
    value = connect.zrange(key, 0, -1)
    cookies = value[0].decode('utf-8')[:-1] if value else ''
    return cookies, key

def get_other_cookies(db=14):
    """
    获取非vip的cookie
    :param db:
    :return:
    """
    connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
    keys = connect.keys()
    key = random.choice(keys)
    if key in [b'15853585853', b'13022721916', b'13375358581']:
        one_key = random.choice(keys)
    else:
        one_key = key

    value = connect.zrange(one_key, 0, -1)
    cookies = value[0].decode('utf-8')[:-1] if value else ''
    return cookies


def get_vip_cookies(db=14):
    """
    获取vip cookie
    :param db:
    :return:
    """
    connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
    keys = ["15853585853", "13022721916", "13375358581"]
    key = random.choice(keys)
    value = connect.zrange(key, 0, -1)
    cookies = value[0].decode('utf-8')[:-1] if value else ''
    # print(cookies)
    return cookies

def get_one_vip_cookie(db=14):
    """
    获取单个vip 账号的cookie
    :param db:
    :return:
    """
    connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
    value = connect.zrange('13375358581', 0, -1)
    cookies = value[0].decode('utf-8')[:-1] if value else ''
    return cookies

def add_companys_id(name, value, db=15):
    """
    向redis添加企业名和企业id
    :param name:
    :param value:
    :param db:
    :return:
    """
    connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
    connect.set(name, value)

def get_companys_id(name, db=15):
    """
    获取企业对应id
    :param name:
    :param db:
    :return:
    """
    connect = redis.Redis(host=HOST, port=6379, db=db, password=PASSWD)
    value = connect.get(name)
    company_id = value.decode('utf-8') if value else ''
    return company_id

def get_tianyan_id(url, name, headers):
    """
    如果redis没有企业id  就来这搜索然后添加
    :param url:
    :param name:
    :param headers:
    :return:
    """
    print('*'*50)
    response = requests.get(url, headers=headers)
    content = response.text
    soup1 = etree.HTML(content)
    if soup1.xpath('//div[@class="search-item sv-search-company"][1]/div[@class="search-result-single   "]/div[@class="content"]/div[@class="header"]/a/@href'):
        url2 = "".join(soup1.xpath('//div[@class="search-item sv-search-company"][1]/div[@class="search-result-single   "]/div[@class="content"]/div[@class="header"]/a/@href'))
        # company_name = "".join(soup1.xpath('//div[@class="search-item sv-search-company"][1]/div[@class="search-result-single   "]/div[@class="content"]/div[@class="header"]/a//text()'))
        company_id = url2.split('/')[-1]
        add_companys_id(name, company_id)
        return url2, company_id
    else:
        return 'https://www.tianyancha.com'