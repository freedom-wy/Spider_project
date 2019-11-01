import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class LiquidatingInfo(BaseSpider):
    """
    清算信息爬虫
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
        # 清算组成员
        member = ''.join(self.get_xpath('./tr[2]/td[2]//text()', html=tr))
        # 清算组负责人
        manager = ''.join(self.get_xpath('./tr[1]/td[2]//text()', html=tr))

        kwargs = {
            'member': member,
            'manager': manager,
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('member', 'manager', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_liquidating_info {keys} value {values};'
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
        try:
            url = f'https://www.tianyancha.com/pagination/clearingCount.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table -striped-col"]/tbody', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')

        except Exception as e:
            print(f'类 - - {LiquidatingInfo.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
