import json
import aiohttp
import asyncio

from utils.Base_spider import BaseSpider


class KtannouncementSpider(BaseSpider):
    """
    开庭公告爬虫
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
        json_data = json.loads(self.get_xpath('.//script/text()', html=tr)[0])
        kwargs = {
            'startDate': json_data.get('startDate', '-'),
            'plaintiff_name': '-'.join([data.get('name') for data in json_data.get('plaintiff')]),
            'courtroom': json_data.get('courtroom', '-'),
            'caseReason': json_data.get('caseReason', '-'),
            'court': json_data.get('court', '-'),
            'litigant': json_data.get('litigant', '-'),
            'judge': json_data.get('judge', '-'),
            'contractors': json_data.get('contractors', '-'),
            'caseNo': json_data.get('caseNo', '-'),
            'defendant_name': '-'.join([data.get('name') for data in json_data.get('defendant')]),
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('startDate', 'plaintiff_type', 'plaintiff_id', 'plaintiff_name', 'courtroom', 'caseReason', 'court',
               'litigant', 'judge', 'contractors', 'caseNo', 'defendant_type', 'defendant_id', 'defendant_name',
               'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_ktannouncement_info {keys} value {values};'
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
        #     f'https://www.tianyancha.com/pagination/announcementcourt.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
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
            url = f'https://www.tianyancha.com/pagination/announcementcourt.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=await resp.text())
                    await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
        except Exception as e:
            print(f'类 - - {KtannouncementSpider.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
