import time
import random
from multiprocessing.pool import ThreadPool

import requests
from lxml import etree

from utils.get_cookies import get_cookies
from configration import CLASS_LIST, CLASS_INFO_DICT, USER_AGENT_LIST


class Scheduling(object):
    """
    调度模块
    对天眼查搜索页数据操作，先爬取对应公司名以及id，可以减少每个维度的操作
    """

    def __init__(self):
        # 对应的维度唯一id
        self.class_list = CLASS_LIST
        # 对应每个公司的所有维度，包括抽取规则，分页，以及条数，和对应的方法
        self.dimension_list = CLASS_INFO_DICT.get('data')
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": get_cookies(),
            "Host": "www.tianyancha.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(USER_AGENT_LIST)
        }

    def download(self, url):
        """
        调度下载
        :return:
        """
        return requests.get(url, headers=self.headers)

    def get_xpath(self, xpath, response=None, html=None):
        """
        xpath解析模块
        :param xpath: xpath
        :param response: 是网页的情况下
        :param html: 之前已经有了xpath
        :return:
        """
        if response:
            html = etree.HTML(response)
            resp = html.xpath(xpath)
        else:
            resp = html.xpath(xpath)

        return resp

    def parse(self, response):
        """
        调度解析
        :return:
        """
        rule_id = '//div[@class="result-list sv-search-container"]/div[1]/div[@class="search-result-single   "]/@data-id'
        rule_name = '//div[@class="result-list sv-search-container"]/div[1]/div[@class="search-result-single   "]//a[@class="name "]//text()'
        vip_rule_id = '//div[@class="result-list sv-search-container"]/div[1]/div[@class="search-result-single   -hasown"]/@data-id'
        vip_rule_name = '//div[@class="result-list sv-search-container"]/div[1]/div[@class="search-result-single   -hasown"]//a[@class="name "]//text()'
        # 获取公司id
        result = self.get_xpath(
            rule_id + ' | ' + vip_rule_id, response)
        # 获取公司名
        name = self.get_xpath(
            rule_name + ' | ' + vip_rule_name,
            response)
        data_id = result[0] if result else ''
        company_name = name[0] if name else ''
        return data_id, company_name

    def parse_detail(self, data_id, company_name):
        """
        获取公司详情页，将公司名和对应的id以及各个维度的信息填充进去
        :param data_id: 公司id
        :param company_name:  公司名称
        :return:
        """
        url = f'https://www.tianyancha.com/company/{data_id}'
        resp = self.download(url)
        html = etree.HTML(resp.text)
        CLASS_INFO_DICT['company_name'] = company_name
        CLASS_INFO_DICT['company_id'] = data_id
        data = self.dimension_list
        # 遍历维度列表，取出每个维度的对应xpath进行抽取
        for xp in self.class_list:
            total_num_xpath = data.get(xp).get('total_num_xpath')
            num = self.get_xpath(total_num_xpath, html=html)
            total_num = num[0] if num else 10
            # 将总条数填充进去
            data.get(xp)['total_num'] = total_num
            data.get(xp)['response'] = resp

    def main(self, company_name):
        """
        对构造公司id和公司名函数调度
        :param company_name:
        :return:
        """
        start_time = time.time()
        resp = self.download(f'https://www.tianyancha.com/search?key={company_name}')
        # 解析出公司名和id
        data_id, company_name = self.parse(resp.text)
        # 对公司详情页进行爬去填充
        self.parse_detail(data_id, company_name)
        end_time = time.time()
        print('填充时间:', end_time - start_time)

    def run(self, company_name, thread_num=16):
        """
        总调度模块
        :param company_name: 需要爬取的公司名，全称
        :param thread_num:  需要开启的线程数，默认16个线程
        :return:
        """
        # 现将数据填充
        start_time = time.time()
        self.main(company_name)
        pool = ThreadPool(thread_num)
        # 对每个维度列表取出对应的维度函数及信息
        for dimension_id in self.class_list:
            data = self.dimension_list.get(dimension_id)
            # 取出对应id
            company_id = CLASS_INFO_DICT.get('company_id')
            # 取出对应的维度方法
            func = data.get('func')
            # 取出总条数
            total_num = data.get('total_num')
            # 取出一页多少条
            one_page = data.get('one_page')
            # 对于没有分页的数据，用详情页爬取
            resp = data.get('response')
            status = data.get('status')
            print(company_name, company_id, total_num, one_page)
            # 进行线程爬取
            pool.apply_async(func=func.run, args=(company_name, company_id, int(total_num), one_page, resp, status))

        pool.close()
        pool.join()
        end_time = time.time()
        print('运行时间:', end_time - start_time)


if __name__ == '__main__':
    sche = Scheduling()
    sche.run('中国石油天然气股份有限公司')
    # sche.main('中国石油天然气股份有限公司')
