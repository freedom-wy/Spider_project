import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class CompanyPublic(BaseSpider):
    """
    股东及出资信息（公司公示）
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    def detail_one_parse(self, tr, company_name, company_id):
        """
        单独解析一个tr
        :param tr:
        :param company_name:
        :param company_id:
        :return:
        """
        # 股东发起人
        name = ''.join(self.get_xpath('./td[2]//td[2]//text()', html=tr))
        # 持股比例
        capital_percent = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 认缴金额
        capital_amomon = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 认缴时间
        capital_time = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 实缴金额
        capitalActl_amomon = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 实缴时间
        capitalActl_time = ''.join(self.get_xpath('./td[7]//text()', html=tr))
        # logo
        logo = ''.join(self.get_xpath('./td[2]//td[1]//img/@data-src', html=tr))

        kwargs = {
            'name': name,
            'capital_percent': capital_percent,
            'capital_amomon': capital_amomon,
            'capital_time': capital_time,
            'capitalActl_amomon': capitalActl_amomon,
            'capitalActl_time': capitalActl_time,
            'logo': logo,
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('capital_amomon', 'capital_paymet', 'capital_time', 'capital_percent', 'name', 'capitalActl_amomon',
               'capitalActl_paymet', 'capitalActl_time', 'logo', 'type', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_company_public {keys} value {values};'
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
        #     f'https://www.tianyancha.com/pagination/holderList.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
        # # 获取所有的trs
        # try:
        #     trs = self.get_xpath('//table[@class="table multi-table"]/tbody/tr', response=resp.text)
        #     # 详情解析
        #     # self.detail_parse(trs, company_name)
        #     # 对一个tr进行解析
        #     for tr in trs:
        #         self.detail_one_parse(tr, company_name, company_id)
        #
        # except Exception as e:
        #     pass

        try:
            url = f'https://www.tianyancha.com/pagination/holderList.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    trs = self.get_xpath('//table[@class="table multi-table"]/tbody/tr', response=await resp.text())
                    await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
        except Exception as e:
            print(f'类 - - {CompanyPublic.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
