import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class ShareStructure(BaseSpider):
    """
    股本结构爬虫
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
        # 时间
        pub_date = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 总股本
        share_all = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # A股总股本
        ashare_all = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 流通A股
        no_limit_share = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 限售A股
        limit_share = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # H股总股本
        hshare_all = ''.join(self.get_xpath('./td[7]//text()', html=tr))
        # 流通H股
        hno_limit_share = ''.join(self.get_xpath('./td[8]//text()', html=tr))
        # # 限售H股
        hlimit_share = ''.join(self.get_xpath('./td[9]//text()', html=tr))
        # # 变动原因
        change_reason = ''.join(self.get_xpath('./td[10]//text()', html=tr))

        kwargs = {
            'company_name': company_name,
            'company_id': company_id,
            'year': year,
            'pub_date': pub_date,
            'share_all': share_all,
            'ashare_all': ashare_all,
            'no_limit_share': no_limit_share,
            'limit_share': limit_share,
            'hshare_all': hshare_all,
            'hno_limit_share': hno_limit_share,
            'hlimit_share': hlimit_share,
            'change_reason': change_reason
        }

        tup = ('pub_date', 'change_reason', 'share_all', 'no_limit_share', 'limit_share', 'ashare_all', 'hno_limit_share',
               'hlimit_share', 'hshare_all', 'company_name', 'company_id', 'year')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_share_structure {keys} value {values};'
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
        # years = self.get_xpath('//div[@id="nav-main-shareStructureNum"]//div[@class="content"]/div/text()', response=resp.text)
        # try:
        #     for index, year in enumerate(years):
        #         result = self.download(f'https://www.tianyancha.com/stock/shareStructure.xhtml?graphId={company_id}&index={index}&time={year}&_={self.get_now_timestamp()}')
        #         trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=result.text)
        #         for tr in trs:
        #             self.detail_one_parse(tr, company_name, company_id, year)
        #
        # except Exception as e:
        #     pass

        try:
            years = self.get_xpath('//div[@id="nav-main-shareStructureNum"]//div[@class="content"]/div/text()',
                                   response=resp.text)
            async with aiohttp.ClientSession() as session:
                for index, year in enumerate(years):
                    url = f'https://www.tianyancha.com/stock/shareStructure.xhtml?graphId={company_id}&index={index}&time={year}&_={self.get_now_timestamp()}'
                    async with session.get(url, headers=self.get_headers) as resp:
                        trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=await resp.text())
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id, year) for tr in trs])
        except Exception as e:
            print(f'类 - - {ShareStructure.__name__} - - 异步请求出错：', e)

if __name__ == '__main__':
    pass