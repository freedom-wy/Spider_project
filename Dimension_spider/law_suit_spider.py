import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class LawSuit(BaseSpider):
    """
    法律诉讼爬虫
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
        # 发布日期
        submittime = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 案件名称
        title = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 案由
        casereason = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 原告
        plaintiffs = ''.join(self.get_xpath('./td[5]/div[1]//text()', html=tr))
        # 被告
        defendants = ''.join(self.get_xpath('./td[5]/div[2]//text()', html=tr))
        # 案号
        caseno = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 详情url
        url = ''.join(self.get_xpath('./td[7]/a/@href', html=tr))

        kwargs = {
            'submittime': submittime,
            'title': title,
            'casereason': casereason,
            'plaintiffs': plaintiffs,
            'defendants': defendants,
            'caseno': caseno,
            'url': url,
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('company_name', 'company_id', 'plaintiffs', 'court', 'casereason', 'url', 'caseno', 'title', 'abstracts',
               'submittime', 'lawsuitUrl', 'casetype', 'doctype', 'agent', 'thirdParties', 'defendants')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_law_suit_info {keys} value {values};'
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
        #     f'https://www.tianyancha.com/pagination/lawsuit.xhtml?ps={ps}&pn={pn}&name={company_name}&_={self.get_now_timestamp()}')
        # # 获取所有的trs
        # try:
        #     trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=resp.text)
        #     # 详情解析
        #     # self.detail_parse(trs, company_name)
        #     # 对一个tr进行解析
        #     for tr in trs:
        #         self.detail_one_parse(tr, company_name, company_id)
        #
        # except Exception as e:
        #     pass

        try:
            url = f'https://www.tianyancha.com/pagination/lawsuit.xhtml?ps={ps}&pn={pn}&name={company_name}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=await resp.text())
                    await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
        except Exception as e:
            print(f'类 - - {LawSuit.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
