# -*- coding: utf-8 -*-
import scrapy
import pymysql
import redis

from ..settings import INFO, INSERT_INFO
from ..items import TycProjectItem


class BaseInfoSpider(scrapy.Spider):
    name = 'base_info'
    # allowed_domains = ['www.tianyancha.com']
    start_urls = ['http://www.tianyancha.com/']

    insert_connect = pymysql.connect(**INSERT_INFO)
    insert_cur = insert_connect.cursor()

    connection = pymysql.connect(**INFO)
    cur = connection.cursor()

    redis_connect = redis.Redis(host='127.0.0.1', db=13)

    def start_requests(self):
        keys = self.redis_connect.keys()
        for key in keys:
            md5_key = key.decode('utf-8')
            name = self.redis_connect.get(md5_key)
            company_name = name.decode('utf-8') if name else None
            url = f'https://www.tianyancha.com/search?key={company_name}'
            yield scrapy.Request(url, callback=self.parse, meta={'company_name': company_name, 'md5_key': md5_key})

    def start_requests_other(self):
        # 获取所有数据库中的id，进行爬取
        count = self._get_mysql_data_count
        for id in range(1, count + 1):
            # 拿到公司名
            md5_key, company_name = self.get_company_name(id)
            # 判断第二张表是否存在公司数据
            if not self.exists_company(company_name):
                url = f'https://www.tianyancha.com/search?key={company_name}'
                yield scrapy.Request(url, callback=self.parse, meta={'company_name': company_name, 'md5_key': md5_key})

    def parse(self, response):
        company_name = response.meta.get('company_name')
        md5_key = response.meta.get('md5_key')
        href = response.xpath('//div[@class="search-item sv-search-company"][1]/div[@class="search-result-single   "]//a[@class="name "]/@href | //div[@class="search-item sv-search-company"][1]/div[@class="search-result-single   -hasown"]//a[@class="name "]/@href')
        item = TycProjectItem()
        if href:
            url = href.extract_first()
            pid = url.split('/')[-1]
            print(url, pid)
            item['company_id'] = pid
            item['company_name'] = company_name
            item['source'] = 'XL'
            yield scrapy.Request(url, callback=self.detail_url, meta={'item': item, 'md5_key': md5_key})
        else:
            self.logger.info(f'{company_name} - - 数据抓取失败')

    def detail_url(self, response):
        trs = response.xpath('//div[@id="_container_baseInfo"]/table[@class="table -striped-col -border-top-none -breakall"]/tbody/tr')
        # print(trs)
        item = response.meta.get('item')
        md5_key = response.meta.get('md5_key')
        for tr in trs:
            tds = tr.xpath('./td')
            if len(tds) > 2:
                td_k1 = tds[0].xpath('.//text()')
                key1 = self.comparison(td_k1.extract_first()) if td_k1 else '-'
                td_v2 = tds[1].xpath('.//text()')
                value1 = td_v2.extract_first() if td_v2 else '-'

                td_k3 = tds[2].xpath('.//text()')
                key2 = self.comparison(td_k3.extract_first()) if td_k3 else '-'
                td_v4 = tds[3].xpath('.//text()')
                value2 = td_v4.extract_first() if td_v4 else '-'

                item[key1] = value1
                item[key2] = value2
            else:
                td_k5 = tds[0].xpath('.//text()')
                key1 = self.comparison(td_k5.extract_first()) if td_k5 else '-'
                td_v5 = tds[1].xpath('.//text()')
                value1 = td_v5.extract_first() if td_v5 else '-'

                item[key1] = value1

        self.redis_connect.delete(md5_key)
        yield item

    def get_company_name(self, id):
        """
        获取对应id的企业，自增id
        :param id:
        :return:
        """
        try:
            self.cur.execute(f'select Md5Key, entName from company_basc_info where col_id={id};')
            result = self.cur.fetchone()
            md5_key = result[0]
            company_name = result[1]
            return md5_key, company_name

        except Exception as e:
            self.connection.rollback()

    def exists_company(self, company_name):
        """
        判断企业是否已经存在于第二张数据表
        :param company_name:
        :return:
        """
        try:
            self.insert_cur.execute(f'SELECT id FROM das_tm_base_info where company_name = "{company_name}";')
            status = self.insert_cur.fetchone()

        except Exception as e:
            self.insert_cur.execute(f'SELECT id FROM das_tm_base_info where company_name = "{company_name}";')
            status = self.insert_cur.fetchone()

        return status

    @property
    def _get_mysql_data_count(self):
        """
        获取mysql总数
        :return:
        """
        try:
            self.cur.execute('select count(col_id) from company_basc_info;')
            count = int(self.cur.fetchone()[0])
        except:
            self.cur.execute('select count(col_id) from company_basc_info;')
            count = int(self.cur.fetchone()[0])

        return count

    def comparison(self, key):
        """
        字段替换
        :param key:
        :return:
        """
        keys = {
            '企业id': 'company_id',
            '企业名': 'company_name',
            '注册资本': 'reg_capital',
            '实缴资本': 'actual_capital',
            '成立日期': 'estiblish_time',
            '经营状态': 'reg_status',
            '统一社会信用代码': 'credit_code',
            '工商注册号': 'reg_number',
            '纳税人识别号': 'tax_number',
            '组织机构代码': 'org_number',
            '公司类型': 'company_org_type',
            '行业': 'industry',
            '核准日期': 'approved_time',
            '登记机关': 'reg_institute',
            '营业期限': 'operating_period',
            '纳税人资质': 'tax_payer',
            '人员规模': 'staff_num_range',
            '参保人数': 'social_staff_num',
            '曾用名': 'history_names',
            '英文名称': 'property3',
            '注册地址': 'reg_location',
            '经营范围': 'business_scope',
        }

        return keys.get(key)
