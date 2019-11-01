import re
import aiohttp
import asyncio

from utils.Base_spider import BaseSpider


class TaxationOffences(BaseSpider):
    """
    税收违法详情爬虫
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
        info = ''.join(self.get_xpath('./td[5]/span/@onclick', html=tr))
        zid = ''.join(re.findall(r'openTaxContraventionDetail\("(.*?)"\)', info))
        url = f'https://www.tianyancha.com/company/getTaxContraventionDetail.json?id={zid}'
        async with session.get(url, headers=self.set_x_auth_token) as resp:
            data = await resp.json()
            kwargs = {'company_name': company_name, 'company_id': company_id}
            kwargs.update(data.get('data'))
            tup = ('res_person_id_type', 'res_person_sex', 'abnormal_id', 'address', 'responsible_department',
                   'res_department_name', 'taxpayer_code', 'case_info', 'legal_person_sex', 'case_type',
                   'legal_person_id_number', 'res_person_name', 'res_department_sex', 'taxpayer_name',
                   'legal_person_id_type', 'publish_time', 'legal_person_name', 'res_person_id_number',
                   'taxpayer_number', 'department', 'res_department_id_type', 'res_department_id_number', 'company_name',
                   'company_id')
            values, keys = self.structure_sql_statement(tup, kwargs)
            sql = f'insert into das_tm_taxation_offences_detail {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/taxContraventions.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(
                            *[self.detail_one_parse(tr, company_name, company_id, session) for tr in trs])
                    else:
                        print('数据为空')
        except Exception as e:
            print(f'类 - - {TaxationOffences.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
