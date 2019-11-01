import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class JudicialSale(BaseSpider):
    """
    司法拍卖爬虫
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
        # 公告日期
        pubTime = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 拍卖公告
        title = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 拍卖标的
        auction_title = ''.join(self.get_xpath('./td[4]/div[1]//text()', html=tr))
        # 起拍价格
        initial_price = ''.join(self.get_xpath('./td[4]/div[2]//text()', html=tr)).replace('起拍价格：', '')
        # 评估价格
        consult_price = ''.join(self.get_xpath('./td[4]/div[3]//text()', html=tr)).replace('评估价格：', '')
        # 执行法院
        court = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 详情url
        url = ''.join(self.get_xpath('./td[6]/a/@href', html=tr))

        kwargs = {
            'company_name': company_name,
            'company_id': company_id,
            'pubTime': pubTime,
            'title': title,
            'auction_title': auction_title,
            'initial_price': initial_price,
            'consult_price': consult_price,
            'court': court,
            'url': url
        }

        tup = ('pubTime', 'detail', 'consult_price', 'initial_price', 'title', 'jid',
               'court', 'scopeDate', 'url', 'auction_title', 'introduction', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_judicial_sale_info {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/judicialSale.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')
        except Exception as e:
            print(f'类 - - {JudicialSale.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
