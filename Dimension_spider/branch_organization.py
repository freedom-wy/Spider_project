import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class BranchOrganization(BaseSpider):
    """
    十大股东爬虫
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
        # logo
        logo = ''.join(self.get_xpath('./td[2]//td[1]//img/@data-src', html=tr))
        # 分支机构名
        name = ''.join(self.get_xpath('./td[2]//td[2]//text()', html=tr))
        # 成立日期
        estiblishTime = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 经营状态
        regStatus = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 负责人
        legalPersonName = ''.join(self.get_xpath('./td[3]//td[2]//text()', html=tr))

        kwargs = {
            'logo': logo,
            'name': name,
            'estiblishTime': estiblishTime,
            'regStatus': regStatus,
            'legalPersonName': legalPersonName,
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('logo', 'alias', 'estiblishTime', 'regStatus', 'legalPersonName', 'category',
               'regCapital', 'company_name', 'company_id', 'base', 'personType', 'name')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_branch_organization_info {keys} value {values};'
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
        #     result = self.download(
        #         f'https://www.tianyancha.com/pagination/branch.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
        #     trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=result.text)
        #     for tr in trs:
        #         self.detail_one_parse(tr, company_name, company_id)
        # except Exception as e:
        #     pass

        try:
            url = f'https://www.tianyancha.com/pagination/branch.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=await resp.text())
                    await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])

        except Exception as e:
            print(f'类 - - {BranchOrganization.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
