# Base爬虫
# from gevent import monkey
# monkey.patch_all()
import gevent

import math
from datetime import datetime

import asyncio
import aiohttp
import requests
from lxml import etree

from utils.get_cookies import get_cookies, get_vip_cookies
from utils.operating_mysql import OperatingMysql


class BaseSpider(object):
    """
    基爬虫
    """

    def __init__(self, *args, **kwargs):
        self.cookie = kwargs.pop('cookie', None)
        self.operating = OperatingMysql()

    async def aiohttp_download(self, url, method='GET', headers=None, proxies=None, cookies=None, data=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                pass

    @property
    def set_x_auth_token(self) -> dict:
        """
        向headers中设置x-auth-token
        :return:
        """
        cookies = {
            'version': 'TYC-Web',
            'X-AUTH-TOKEN': ''
        }
        headers = self.get_headers
        one_cookies = headers.get('Cookie').split(';')
        cookies_tup = [k.split('=') for k in one_cookies]
        for token in cookies_tup:
            if token[0] == 'auth_token':
                cookies['X-AUTH-TOKEN'] = token[1]
                break
        cookies.update(headers)
        return cookies

    @property
    def get_headers(self):
        """
        获取headers
        :return:
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": get_vip_cookies() if self.cookie == 'vip' else get_cookies(),
            "Host": "www.tianyancha.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        }

        return headers

    def download(self, url, method='GET', headers=None, proxies=None, cookies=None, data=None):
        """
        下载器
        :param url:
        :param headers:
        :param proxies:
        :param cookies:
        :return:
        """
        headers = headers if headers else self.get_headers
        if method == 'GET':
            resp = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, params=data)
        elif method == 'POST':
            resp = requests.post(url, headers=headers, cookies=cookies, proxies=proxies, data=data)
        else:
            resp = requests.options(url, headers=headers, cookies=cookies, proxies=proxies, params=data)

        return resp

    def get_xpath(self, xpath, response=None, html=None):
        """
        xpath解析模块
        :param xpath:
        :param response:
        :param html:
        :return:
        """
        if response:
            html = etree.HTML(response)
            resp = html.xpath(xpath)
        else:
            resp = html.xpath(xpath)

        return resp

    def structure_sql_statement(self, tup, dic):
        """
        构造sql语句
        :param tup:
        :param dic:
        :return:
        """
        tup_val = []
        for key in tup:
            data = dic.get(key)
            tup_val.append(data if data else '-')

        tup = str(tup).replace("'", '')

        return tuple(tup_val), tup

    def page_total(self, total_num, one_page):
        """
        获取页数
        :return:
        """
        return math.ceil(total_num / one_page)

    def get_now_timestamp(self):
        """
        返回当前十三位时间戳
        :return:
        """
        return int(datetime.now().timestamp() * 1000)

    async def parse(self, company_id, company_name, ps=20, pn=1, resp=None):
        pass

    async def main(self, company_name: str, company_id: str, total_num: int, one_page: int, resp):
        """
        run函数
        :param company_name:
        :param company_id:
        :param total_num:
        :param one_page:
        :param resp:
        :return:
        """
        page = self.page_total(total_num, one_page)
        tracks = [self.parse(company_id, company_name, one_page, pn, resp) for pn in range(1, page + 1)]
        await asyncio.gather(*tracks)

    def run(self, company_name: str, company_id: str, total_num: int, one_page: int, resp, status):
        if status == 'async':
            asyncio.run(self.main(company_name, company_id, total_num, one_page, resp))
        elif status == 'coroutine':
            page = self.page_total(total_num, one_page)
            spawn_list = []
            for pn in range(1, page + 1):
                # 开启携程
                spawn_list.append(gevent.spawn(self.parse, company_id, company_name, one_page, pn, resp))

            gevent.joinall(spawn_list)


if __name__ == '__main__':
    base = BaseSpider()
    a = base.page_total(22, 20)
    print(a)
