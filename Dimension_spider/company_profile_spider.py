import asyncio
import aiohttp

from utils.Base_spider import BaseSpider

roule = {
    '公司全称': 'company_name',
    '英文名称': 'eng_name',
    '上市曾用名': 'used_name',
    '工商登记': 'actual_capital',
    '注册资本': 'registered_capital',
    '所属行业': 'industry',
    '董事长': 'chairman_name',
    '董秘': 'secretaries_name',
    '法定代表人': 'legal_name',
    '总经理': 'general_manager_name',
    '员工人数': 'employees_num',
    '管理人员人数': 'industry',
    '控股股东': 'controlling_shareholder',
    '实际控制人': 'actual_controller',
    '最终控制人': 'final_controller',
    '主营业务': 'main_business',
    '': ''
}


class CompanyProfile(BaseSpider):
    """
    公司简介爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    def detail_one_parse(self, **kwargs):
        """
        单独解析一个tr
        :return:
        """
        tup = ('legal_id', 'legal_cType', 'legal_name', 'chairman_id', 'chairman_cType', 'chairman_name', 'postal_code',
               'controlling_shareholder', 'fax', 'website', 'employees_num', 'main_business', 'code', 'company_name',
               'company_id', 'registered_capital', 'used_name', 'area', 'address', 'name', 'general_manager_id',
               'general_manager_cType', 'general_manager_name', 'actual_controller', 'final_controller', 'industry',
               'secretaries_id', 'secretaries_cType', 'secretaries_name', 'product_name', 'eng_name', 'introduction',
               'mobile')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_company_profile_info {keys} value {values};'
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
        #     trs = self.get_xpath('//div[@id="nav-main-stockNum"]//table/tbody/tr', response=resp.text)
        #     kwargs = {
        #         'company_id': company_id
        #     }
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
            trs = self.get_xpath('//div[@id="nav-main-stockNum"]//table/tbody/tr', response=resp.text)
            li = []
            async with aiohttp.ClientSession() as session:
                kwargs = {
                    'company_id': company_id
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
            print(f'类 - - {CompanyProfile.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
