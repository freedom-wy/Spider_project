import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class ForeignInvestmentSpider(BaseSpider):
    """
    对外投资爬虫
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
        # 被投资企业名
        name = ''.join(self.get_xpath('./td[2]//td[1]//img[@class="img expand-img"]/@alt', html=tr))
        # 法定代表人
        legalPersonName = ''.join(self.get_xpath('./td[3]//td[2]/div[1]//text()', html=tr))
        # 成立日期
        estiblishTime = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 投资数额
        amount = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 投资比例
        percent = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 经营状态
        regstatus = ''.join(self.get_xpath('./td[7]//text()', html=tr))

        kwargs = {
            'name': name,
            'legalPersonName': legalPersonName,
            'estiblishTime': estiblishTime,
            'amount': amount,
            'percent': percent,
            'regstatus': regstatus,
            'company_id': company_id,
            'company_name': company_name
        }
        tup = ('orgType', 'business_scope', 'percent', 'regStatus', 'estiblishTime', 'legalPersonName', 'type', 'amount', 'category', 'regCapital', 'name', 'base', 'creditCode', 'personType', 'alias', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_inverst_info {keys} value {values};'
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
        # resp = self.download(f'https://www.tianyancha.com/pagination/invest.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
        # # 获取所有的trs
        # try:
        #     trs = self.get_xpath('//table[@class="table -breakall"]/tbody/tr', response=resp.text)
        #     # 对一个tr进行解析
        #     for tr in trs:
        #         self.detail_one_parse(tr, company_name, company_id)
        # except Exception as e:
        #     pass

        try:
            url = f'https://www.tianyancha.com/pagination/invest.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table -breakall"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('数据为空')
        except Exception as e:
            print(f'类 - - {ForeignInvestmentSpider.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass