import asyncio
import aiohttp

from utils.Base_spider import BaseSpider

roule = {
    '总市值': 'tvalue',
    '流通市值': 'flowvalue',
    '成交量': 'tamount',
    '成交额': 'tamount_total',
    '今开': 'topen_price',
    '昨收': 'pprice',
    '最高': 'thigh_price',
    '最低': 'tlow_price',
    '涨停': 'tmax_price',
    '跌停': 'tmin_price',
    '振幅': 'trange',
    '换手': 'tchange',
    '市净率': 'tvaluep',
    '市盈率（动）': 'fvaluep',
    '上市日期': 'listing_date',
    '': ''
}


class StockQuotation(BaseSpider):
    """
    股票行情爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    def detail_one_parse(self, **kwargs):
        """
        单独解析一个tr
        :return:
        """
        tup = ('stock_code', 'company_id', 'stock_name', 'stock_type', 'time_show', 'fvaluep', 'tvalue', 'flowvalue',
               'tvaluep', 'topen_price', 'tamount', 'trange', 'thigh_price', 'tamount_total', 'tchange', 'tlow_price',
               'pprice', 'tmax_price', 'tmin_price', 'hexm_cur_price', 'hexm_float_price', 'hexm_float_rate',
               'company_name', 'listing_date')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_stock_quotation_info {keys} value {values};'
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
        # resp = self.download(
        #     f'https://www.tianyancha.com/company/volatility_num.xhtml?id={company_id}&type=&_={self.get_now_timestamp()}')
        # # 获取所有的trs
        # try:
        #     trs = self.get_xpath('//div[@id="_container_volatilityNum"]/table[@class="table -striped-col"]/tbody/tr',
        #                          response=resp.text)
        #     stock_code = ''.join(self.get_xpath('//span[@class="left"]/span[2]//text()', response=resp.text))[1:-1]
        #     stock_name = ''.join(self.get_xpath('//span[@class="left"]/span[1]//text()', response=resp.text))
        #     time_show = ''.join(self.get_xpath('//div[@class="stock-update-time"]/text()', response=resp.text))
        #     hexm_cur_price = ''.join(self.get_xpath('//span[@class="trend"]/text()', response=resp.text))
        #     hexm_float_price = ''.join(self.get_xpath('//div[@class="trendpart"]/div[1]/text()', response=resp.text))
        #     hexm_float_rate = ''.join(self.get_xpath('//div[@class="trendpart"]/div[2]/text()', response=resp.text))
        #     kwargs = {
        #         'stock_code': stock_code,
        #         'stock_name': stock_name,
        #         'time_show': time_show,
        #         'hexm_cur_price': hexm_cur_price,
        #         'hexm_float_price': hexm_float_price,
        #         'hexm_float_rate': hexm_float_rate,
        #         'company_name': company_name,
        #         'company_id': company_id
        #     }
        #     # 对一个tr进行解析
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
            li = []
            url = f'https://www.tianyancha.com/company/volatility_num.xhtml?id={company_id}&type=&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    trs = self.get_xpath(
                        '//div[@id="_container_volatilityNum"]/table[@class="table -striped-col"]/tbody/tr',
                        response=await resp.text())
                    stock_code = ''.join(self.get_xpath('//span[@class="left"]/span[2]//text()', response=resp.text))[
                                 1:-1]
                    stock_name = ''.join(self.get_xpath('//span[@class="left"]/span[1]//text()', response=resp.text))
                    time_show = ''.join(self.get_xpath('//div[@class="stock-update-time"]/text()', response=resp.text))
                    hexm_cur_price = ''.join(self.get_xpath('//span[@class="trend"]/text()', response=resp.text))
                    hexm_float_price = ''.join(
                        self.get_xpath('//div[@class="trendpart"]/div[1]/text()', response=resp.text))
                    hexm_float_rate = ''.join(
                        self.get_xpath('//div[@class="trendpart"]/div[2]/text()', response=resp.text))
                    kwargs = {
                        'stock_code': stock_code,
                        'stock_name': stock_name,
                        'time_show': time_show,
                        'hexm_cur_price': hexm_cur_price,
                        'hexm_float_price': hexm_float_price,
                        'hexm_float_rate': hexm_float_rate,
                        'company_name': company_name,
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
                    await asyncio.gather(*[self.detail_one_parse(**kwargs) for tr in li])
        except Exception as e:
            print(f'类 - - {StockQuotation.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
