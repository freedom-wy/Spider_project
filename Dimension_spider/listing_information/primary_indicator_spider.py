import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


roule = {
    '基本每股收益(元)': 'basic_eps',
    '扣非每股收益(元)': 'basic_e_ps_net_of_nrgal',
    '稀释每股收益(元)': 'dlt_earnings_per_share',
    '每股净资产(元)': 'net_profit_per_share',
    '每股公积金(元)': 'capital_reserve',
    '每股未分配利润(元)': 'undistri_profit_ps',
    '每股经营现金流(元)': 'operate_cash_flow_ps',
    '营业总收入(元)': 'total_revenue',
    '毛利润(元)': 'accounting_firm_name',
    '归属净利润(元)': 'net_profit_atsopc',
    '扣非净利润(元)': 'profit_nrgal_sq',
    '营业总收入同比增长(%)': 'revenue_yoy',
    '归属净利润同比增长(%)': 'net_profit_atsopc_yoy',
    '扣非净利润同比增长(%)': 'np_atsopc_nrgal_yoy',
    '营业总收入滚动环比增长(%)': 'operating_total_revenue_lrr_sq',
    '归属净利润滚动环比增长(%)': 'net_profit_atsopc_lrr_sq',
    '扣非净利润滚动环比增长(%)': 'profit_deduct_nrgal_lrr_sq',
    '加权净资产收益率(%)': 'wgt_avg_roe',
    '摊薄净资产收益率(%)': 'fully_dlt_roe',
    '摊薄总资产收益率(%)': 'net_interest_of_total_assets',
    '毛利率(%)': 'gross_selling_rate',
    '净利率(%)': 'net_selling_rate',
    '实际税率(%)': 'tax_rate',
    '预收款/营业收入': 'pre_receivableg',
    '销售现金流/营业收入': 'crfgsasr_to_revenue',
    '经营现金流/营业收入': 'accounting_firm_name',
    '总资产周转率(次)': 'total_capital_turnover',
    '应收账款周转天数(天)': 'receivable_turnover_days',
    '存货周转天数(天)': 'inventory_turnover_days',
    '资产负债率(%)': 'asset_liab_ratio',
    '流动负债/总负债(%)': 'current_liab_to_total_liab',
    '流动比率': 'current_ratio',
    '速动比率': 'quick_ratio',
    '': ''
}


class PrimaryIndicator(BaseSpider):
    """
    主要指标爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    async def detail_one_parse(self, **kwargs):
        """
        单独解析一个tr
        :return:
        """
        tup = ('crfgsasr_to_revenue', 'np_atsopc_nrgal_yoy', 'asset_liab_ratio', 'revenue_yoy', 'net_profit_atsopc_yoy',
               'fully_dlt_roe', 'tax_rate', 'receivable_turnover_days', 'pre_receivableg', 'current_ratio',
               'operate_cash_flow_ps', 'show_year', 'gross_selling_rate', 'current_liab_to_total_liab',
               'net_interest_of_total_assets', 'operating_total_revenue_lrr_sq', 'profit_deduct_nrgal_lrr_sq', 'wgt_avg_roe',
               'basic_eps', 'net_selling_rate', 'total_capital_turnover', 'net_profit_atsopc_lrr_sq', 'net_profit_per_share',
               'capital_reserve', 'profit_nrgal_sq', 'inventory_turnover_days', 'total_revenue', 'undistri_profit_ps',
               'dlt_earnings_per_share', 'net_profit_atsopc', 'basic_e_ps_net_of_nrgal', 'company_name', 'company_id',
               'quick_ratio')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_primary_indicator_info {keys} value {values};'
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
        #     trs = self.get_xpath('//div[@id="_container_corpMainIndex"]//table/tbody/tr', response=resp.text)
        #     years = self.get_xpath('//div[@id="_container_corpMainIndex"]//div[@class="data-box"]//'
        #                            'th[@class="text-center"]/text()', response=resp.text)
        #
        #     for num, year in enumerate(years):
        #         kwargs = {
        #             'show_year': year,
        #             'company_name': company_name,
        #             'company_id': company_id
        #         }
        #         for tr in trs:
        #             name = ''.join(self.get_xpath('./td[1]/text()', html=tr))
        #             value = ''.join(self.get_xpath(f'./td[{num+2}]/text()', html=tr))
        #             if name and value:
        #                 key = roule.get(name, '-')
        #                 kwargs[key] = value
        #         self.detail_one_parse(**kwargs)
        #
        # except Exception as e:
        #     pass

        try:
            trs = self.get_xpath('//div[@id="_container_corpMainIndex"]//table/tbody/tr', response=resp.text)
            years = self.get_xpath('//div[@id="_container_corpMainIndex"]//div[@class="data-box"]//'
                                   'th[@class="text-center"]/text()', response=resp.text)
            li = []
            async with aiohttp.ClientSession() as session:
                for num, year in enumerate(years):
                    kwargs = {
                        'show_year': year,
                        'company_name': company_name,
                        'company_id': company_id
                    }
                    for tr in trs:
                        name = ''.join(self.get_xpath('./td[1]/text()', html=tr))
                        value = ''.join(self.get_xpath(f'./td[{num + 2}]/text()', html=tr))
                        if name and value:
                            key = roule.get(name, '-')
                            kwargs[key] = value
                    li.append(kwargs)
            await asyncio.gather(*[self.detail_one_parse(**data) for data in li])
        except Exception as e:
            print(f'类 - - {PrimaryIndicator.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
