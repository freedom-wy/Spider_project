import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class IntellectualProperty(BaseSpider):
    """
    知识产权出质
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
        # 知识产权登记号
        iprCertificateNum = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 名称
        iprName = '-'.join(self.get_xpath('./td[3]//text()', html=tr))
        # 种类
        iprType = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 出质人名称
        pledgorName = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 质权人名称
        pledgeeName = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 职权登记期限
        pledgeRegPeriod = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 状态
        state = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 公示日期
        # 操作

        kwargs = {
            'changeTime': changeTime,
            'changeItem': changeItem,
            'contentBefore': contentBefore,
            'contentAfter': contentAfter,
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('changeItem', 'createTime', 'contentBefore', 'contentAfter', 'changeTime', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_intellectual_property {keys} value {values};'
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
        #         f'https://www.tianyancha.com/pagination/changeinfo.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
        #     trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=result.text)
        #     for tr in trs:
        #         self.detail_one_parse(tr, company_name, company_id)
        # except Exception as e:
        #     pass

        try:
            url = f'https://www.tianyancha.com/pagination/intellectualProperty.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table -breakall"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')

        except Exception as e:
            print(f'类 - - {IntellectualProperty.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
