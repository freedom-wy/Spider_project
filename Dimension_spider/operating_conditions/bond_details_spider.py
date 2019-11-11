import asyncio
import json

import aiohttp

from utils.Base_spider import BaseSpider


class BondDetails(BaseSpider):
    """
    债券信息爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    async def detail_one_parse(self, tr, company_name, company_id):
        """
        单独解析一个tr
        :return:
        """
        script = ''.join(self.get_xpath('./td[7]/script//text()', html=tr))
        kwargs = json.loads(script)
        kwargs.update({'company_name': company_name, 'company_id': company_id})

        tup = ('bondName', 'bondNum', 'bondStopTime', 'bondTimeLimit', 'bondTradeTime', 'bondType', 'calInterestType',
               'createTime', 'creditRatingGov', 'debtRating', 'escrowAgent', 'exeRightTime', 'exeRightType',
               'faceInterestRate', 'faceValue', 'flowRange', 'interestDiff', 'issuedPrice', 'payInterestHZ',
               'planIssuedQuantity', 'publishExpireTime', 'publishTime', 'publisherName', 'realIssuedQuantity',
               'refInterestRate', 'remark', 'startCalInterestTime', 'tip', 'updateTime', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_bond_details {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/bond.xhtml?ps={ps}&pn={pn}&name={company_name}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')
        except Exception as e:
            print(f'类 - - {BondDetails.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
