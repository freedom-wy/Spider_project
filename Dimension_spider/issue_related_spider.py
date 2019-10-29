import asyncio
import aiohttp

from utils.Base_spider import BaseSpider

roule = {
    '成立日期': 'issue_date',
    '上市日期': 'listing_date',
    '发行市盈率': 'ipo_ratio',
    '网上发行日期': 'bstock_cn',
    '发行方式': 'hstock_code',
    '每股面值': 'hstock_cn',
    '发行数量': 'issue_number',
    '发行价格': 'issue_price',
    '募集资金净额': 'accounting_firm_name',
    '实际发行费用': 'accounting_firm_name',
    '预计募资': '预计募资',
    '实际募资': 'actual_raised',
    '网上发行中签率': 'rate',
    '网下发行中签率': 'accounting_firm_name',
    '发行前每股净资产': 'accounting_firm_name',
    '发行后每股净资产': 'accounting_firm_name',
    '发行前总股本': 'accounting_firm_name',
    '发行后总股本': 'accounting_firm_name',
    '上市保荐人': 'listing_sponsor_name',
    '主承销商': 'main_underwriter_name',
    '首日开盘价': 'opening_price',
    '历史沿革': 'history',
    '': ''
}


class IssueRelated(BaseSpider):
    """
    发行相关爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    def detail_one_parse(self, **kwargs):
        """
        单独解析一个tr
        :return:
        """
        tup = ('expected_to_raise', 'main_underwriter_id', 'main_underwriter_type', 'main_underwriter_name', 'history',
               'issue_number', 'issue_price', 'listing_sponsor_id', 'listing_sponsor_type', 'listing_sponsor_name',
               'ipo_ratio', 'rate', 'actual_raised', 'listing_date', 'issue_date', 'opening_price', 'company_name',
               'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_issue_related {keys} value {values};'
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
        #     trs = self.get_xpath('//div[@id="nav-main-issueRelatedNum"]//table/tbody/tr', response=resp.text)
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
            trs = self.get_xpath('//div[@id="nav-main-issueRelatedNum"]//table/tbody/tr', response=resp.text)
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
            print(f'类 - - {IssueRelated.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
