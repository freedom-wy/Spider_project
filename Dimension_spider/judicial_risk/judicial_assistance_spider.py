import asyncio
import aiohttp
import re

from utils.Base_spider import BaseSpider
from utils.func.judicial_func import get_different_roules


class JudicialAssistance(BaseSpider):
    """
    司法协助爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    async def detail_one_parse(self, tr, company_name, company_id, session):
        """
        单独解析一个tr
        :param tr:
        :param company_name:
        :param company_id:
        :param session:
        :return:
        """
        info = ''.join(self.get_xpath('./td[7]/span/@onclick', html=tr))
        zid = ''.join(re.findall(r'openJudicialAidDetail\("(.*?)"\)', info))
        url = f'https://www.tianyancha.com/company/judicialAidDetail.json?id={zid}&_={self.get_now_timestamp()}'
        async with session.get(url, headers=self.set_x_auth_token) as resp:
            data = (await resp.json()).get('data')
            key = list(data.keys())[0]
            kwargs = get_different_roules(data.get(key), key)
            kwargs.update({'company_name': company_name, 'company_id': company_id})

            tup = ('licenseNum', 'assigneeLicenseNum', 'assigneeCid', 'executionDate', 'assigneeLicenseType', 'assignee',
                   'assigneeType', 'assId', 'frozenRemoveDate', 'toDate', 'executeOrderNum', 'equityAmountOther',
                   'period', 'implementationMatters', 'executiveCourt', 'fromDate', 'executeNoticeNum',
                   'executedPersonCid', 'executedPersonType', 'licenseType', 'publicityAate', 'invalidationDate',
                   'invalidationReason', 'equityAmount', 'executedPerson', 'executedPersonHid', 'typeState',
                   'company_name', 'company_id')
            values, keys = self.structure_sql_statement(tup, kwargs)
            sql = f'insert into das_tm_judicial_assistance_details {keys} value {values};'
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
        #     f'https://www.tianyancha.com/pagination/judicialAid.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
        # # 获取所有的trs
        # try:
        #     trs = self.get_xpath('//table[@class="table -sort"]/tbody/tr', response=resp.text)
        #     # 详情解析
        #     # self.detail_parse(trs, company_name)
        #     # 对一个tr进行解析
        #     for tr in trs:
        #         self.detail_one_parse(tr, company_name, company_id)
        #
        # except Exception as e:
        #     pass

        try:
            url = f'https://www.tianyancha.com/pagination/judicialAid.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table -sort"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id, session) for tr in trs])
                    else:
                        print('无数据')
        except Exception as e:
            print(f'类 - - {JudicialAssistance.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
