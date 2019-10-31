import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class HumanHolding(BaseSpider):
    """
    十大股东爬虫
    """
    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    async def detail_one_parse(self, tr, company_name, company_id):
        """
        单独解析一个tr
        :param tr:
        :param company_name:
        :param company_id:
        :return:
        """
        # 最终受益人名称
        name = ''.join(self.get_xpath('./td[2]//td[2]//text()', html=tr))
        # 持股比例
        shareholding_ratio = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        leg = ''.join(self.get_xpath('./td[4]/div/div[2]//text()', html=tr))
        leg_name = ''.join(self.get_xpath('./td[4]/div/span[1]//text()', html=tr))
        leg_company = ''.join(self.get_xpath('./td[4]/div/span[2]//text()', html=tr))
        # 股权链（上）
        equity_chain = leg_name + '-' + leg + '-' + leg_company
        # 股权链（下）
        equity_chain_info = ''.join(self.get_xpath('./td[4]/div/div[3]//text()', html=tr))


        kwargs = {
            'company_name': company_name,
            'company_id': company_id,
            'name': name,
            'shareholding_ratio': shareholding_ratio,
            'equity_chain': equity_chain,
            'equity_chain_info': equity_chain_info,
        }

        tup = ('name', 'shareholding_ratio', 'equity_chain', 'name_company_name', 'company_name', 'company_id',
               'equity_chain_name', 'equity_chain_ratio', 'equity_chain_companyname', 'equity_chain_info')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_human_holding_info {keys} value {values};'
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
        # try:
        #     result = self.download(f'https://www.tianyancha.com/company/holder_holding_analysis.xhtml?id={company_id}&_={self.get_now_timestamp()}')
        #     trs = self.get_xpath('//div[@id="_container_humanholding"]/table/tbody/tr', response=result.text)
        #     for tr in trs:
        #         self.detail_one_parse(tr, company_name, company_id)
        # except Exception as e:
        #     pass

        try:
            url = f'https://www.tianyancha.com/company/holder_holding_analysis.xhtml?id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//div[@id="_container_humanholding"]/table/tbody/tr',
                                         response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')
        except Exception as e:
            print(f'类 - - {HumanHolding.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass