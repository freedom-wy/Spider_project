# -*- coding: utf-8 -*-
import scrapy
import pymysql
import json


class CompanyInfoSpiderSpider(scrapy.Spider):
    name = 'company_info_spider'
    # allowed_domains = ['www.tianyancha.com']
    start_urls = [f'https://www.tianyancha.com/']

    def start_requests(self):
        """
        拿出公司名 发请求
        :return:
        """
        result = self.get_company_name()
        url_list = [f'http://open.api.tianyancha.com/services/open/ic/baseinfo/2.0?name={name}' for name in result]
        for url in url_list:
            # url = f'http://open.api.tianyancha.com/services/open/ic/baseinfo/2.0?name={name}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.text)

    def get_company_name(self):
        """
        将mysql中的数据名导出到json格式
        :return:
        """
        with open('./company_info/spiders/company_list.txt', 'r', encoding='UTF-8') as f:
            result = json.load(f)
        return result['result']