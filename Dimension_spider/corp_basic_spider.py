import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


roule = {
    '总经理': 'general_manager',
    '法定代表人': 'legal_representative',
    '董秘': 'secretary',
    '董事长': 'chairman',
    '证券事务代表': 'sec_representative',
    '独立董事': 'independentDirector',
    '': ''
}


class CorpBasic(BaseSpider):
    """
    重要人员爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    async def detail_one_parse(self, **kwargs):
        """
        单独解析一个tr
        :return:
        """
        tup = ('office_address_cn', 'legal_representative', 'sec_representative', 'chairman', 'business_reg_num',
               'established_date', 'secretary', 'general_manager', 'org_name_en', 'staff_num',
               'company_name', 'reg_address_cn', 'independentDirector', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_corp_basic_info {keys} value {values};'
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
        #     trs = self.get_xpath('//div[@id="_container_corpBasicInfo"]//table/tbody/tr', response=resp.text)
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
        #     self.detail_one_parse(**kwargs)
        #
        # except Exception as e:
        #     pass

        try:
            trs = self.get_xpath('//div[@id="_container_corpBasicInfo"]//table/tbody/tr', response=resp.text)
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
            print(f'类 - - {CorpBasic.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
