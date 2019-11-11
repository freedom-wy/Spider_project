import json

import re
import aiohttp
import asyncio

from utils.Base_spider import BaseSpider


class Certificate(BaseSpider):
    """
    资质证书爬虫
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
        kwargs = {'company_name': company_name, 'company_id': company_id}
        # 发证日期
        startDate = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 证书类型
        certificateName = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 证书编号
        certNo = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 截止日期
        endDate = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        kwargs.update({
            'startDate': startDate,
            'certificateName': certificateName,
            'certNo': certNo,
            'endDate': endDate,
        })
        info = ''.join(self.get_xpath('./td[6]/a/@onclick', html=tr))
        zid = ''.join(re.findall(r"certificatePopup\('(.*?)'\)", info, re.S))
        url = f'https://www.tianyancha.com/company/certificateDetail.json?id={zid}&_={self.get_now_timestamp()}'
        async with session.get(url, headers=self.set_x_auth_token) as resp:
            data = await resp.json()
            kwargs.update({'detail': json.dumps(data.get('data').get('detail'))})
            tup = ('certNo', 'certificateName', 'startDate', 'endDate', 'detail', 'company_name', 'company_id')
            values, keys = self.structure_sql_statement(tup, kwargs)
            sql = f'insert into das_tm_certificate_info {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/certificate.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table -breakall"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(
                            *[self.detail_one_parse(tr, company_name, company_id, session) for tr in trs])
                    else:
                        print('数据为空')
        except Exception as e:
            print(f'类 - - {Certificate.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
