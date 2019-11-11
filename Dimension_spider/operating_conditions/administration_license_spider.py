import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class AdministrationLicense(BaseSpider):
    """
    行政许可（工商信息）爬虫
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
        # 许可文件编号
        licencenumber = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 许可文件名称
        licencename = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 有效期自
        fromdate = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 有效期至
        todate = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 许可机关
        department = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 许可内容
        scope = ''.join(self.get_xpath('./td[7]/div/div//text()', html=tr))

        kwargs = {
            'licencenumber': licencenumber,
            'licencename': licencename,
            'fromdate': fromdate,
            'todate': todate,
            'department': department,
            'scope': scope,
            'company_name': company_name,
            'company_id': company_id
        }
        tup = ('fromdate', 'todate', 'licencenumber', 'scope', 'department', 'licencename',
               'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_administration_license_info {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/licensing.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table -breakall"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')

        except Exception as e:
            print(f'类 - - {AdministrationLicense.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
