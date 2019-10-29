import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class ShareHolder(BaseSpider):
    """
    十大股东爬虫
    """
    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    def detail_one_parse(self, tr, company_name, company_id, year):
        """
        单独解析一个tr
        :param tr:
        :param company_name:
        :param company_id:
        :param year:
        :return:
        """
        # 股东名称
        name = ''.join(self.get_xpath('./td[2]//td[2]//text()', html=tr))
        # 股份类型
        shareType = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 持股数量
        holdingNum = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 持股变化
        compareChange = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 占股本比例
        proportion = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 实际增减持
        actual = ''.join(self.get_xpath('./td[7]//text()', html=tr))

        kwargs = {
            'company_name': company_name,
            'company_id': company_id,
            'year': year,
            'name': name,
            'shareType': shareType,
            'holdingNum': holdingNum,
            'compareChange': compareChange,
            'proportion': proportion,
            'actual': actual
        }
        tup = ('proportion', 'mtenPercent', 'company_id', 'tenPercent', 'type', 'ten_total', 'cType', 'company_name',
               'actual', 'sorting', 'holdingChange', 'holdingNum', 'shareType', 'compareChange', 'publishDate', 'name',
               'year')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_share_holder_info {keys} value {values};'
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
        # years = self.get_xpath('//div[@id="nav-main-topTenNum"]//div[@class="content"]/div/text()', response=resp.text)
        # try:
        #     for index, year in enumerate(years):
        #         result = self.download(f'https://www.tianyancha.com/stock/shareholder.xhtml?graphId={company_id}&index={index}&type=1&time={year}&_={self.get_now_timestamp()}')
        #         trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=result.text)
        #         for tr in trs:
        #             self.detail_one_parse(tr, company_name, company_id, year)
        #
        # except Exception as e:
        #     pass
        try:
            years = self.get_xpath('//div[@id="nav-main-topTenNum"]//div[@class="content"]/div/text()',
                                   response=resp.text)
            async with aiohttp.ClientSession() as session:
                for index, year in enumerate(years):
                    url = f'https://www.tianyancha.com/stock/shareholder.xhtml?graphId={company_id}&index={index}&type=1&time={year}&_={self.get_now_timestamp()}'
                    async with session.get(url, headers=self.get_headers) as resp:
                        trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=await resp.text())
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id, year) for tr in trs])
        except Exception as e:
            print(f'类 - - {ShareHolder.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass