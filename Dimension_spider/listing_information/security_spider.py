import asyncio
import aiohttp

from utils.Base_spider import BaseSpider

roule = {
    'A股代码': 'astock_code',
    'A股简称': 'astock_cn',
    'B股代码': 'bstock_code',
    'B股简称': 'bstock_cn',
    'H股代码': 'hstock_code',
    'H股简称': 'hstock_cn',
    '证券类别': 'sec_type',
    '律师事务所': 'law_firm_name',
    '会计师事务所': 'accounting_firm_name',
    '': ''
}


class Security(BaseSpider):
    """
    证券信息爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    async def detail_one_parse(self, **kwargs):
        """
        单独解析一个tr
        :return:
        """
        tup = ('law_firm_name', 'sec_type', 'accounting_firm_name', 'astock_cn', 'astock_code', 'bstock_cn',
               'bstock_code', 'hstock_cn', 'hstock_code', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_security_info {keys} value {values};'
        print(sql)
        self.operating.save_mysql(sql)

    async def parse(self, company_id, company_name, ps=20, pn=1, resp=None):
        """
        对应的ajax接口爬取
        :param company_id:
        :param company_name:
        :param ps:
        :param pn:
        :param resp:
        :return:
        """
        # 获取所有的trs
        # try:
        #     trs = self.get_xpath('//div[@id="_container_secBasicInfo"]//table/tbody/tr', response=resp.text)
        #     kwargs = {
        #         'company_id': company_id,
        #         'company_name': company_name
        #     }
        #
        #     for tr in trs:
        #         name_left = roule[''.join(self.get_xpath('./td[1]/text()', html=tr))]
        #         value_left = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        #         name_right = roule[''.join(self.get_xpath('./td[3]/text()', html=tr))]
        #         value_right = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        #         kwargs[name_left] = value_left
        #         kwargs[name_right] = value_right
        #
        #     self.detail_one_parse(**kwargs)
        #
        # except Exception as e:
        #     pass

        try:
            trs = self.get_xpath('//div[@id="_container_secBasicInfo"]//table/tbody/tr', response=resp.text)
            li = []
            async with aiohttp.ClientSession() as session:
                kwargs = {
                    'company_id': company_id,
                    'company_name': company_name
                }

                for tr in trs:
                    name_left = roule[''.join(self.get_xpath('./td[1]/text()', html=tr))]
                    value_left = ''.join(self.get_xpath('./td[2]//text()', html=tr))
                    name_right = roule[''.join(self.get_xpath('./td[3]/text()', html=tr))]
                    value_right = ''.join(self.get_xpath('./td[4]//text()', html=tr))
                    kwargs[name_left] = value_left
                    kwargs[name_right] = value_right
                li.append(kwargs)
            await asyncio.gather(*[self.detail_one_parse(**data) for data in li])
        except Exception as e:
            print(f'类 - - {Security.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
