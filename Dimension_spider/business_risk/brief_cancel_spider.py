import asyncio
import json

import aiohttp

from utils.Base_spider import BaseSpider


class BriefCancel(BaseSpider):
    """
    简易注销爬虫
    """

    def __init__(self, *args, **kwargs):
        # 继承父类的方法
        super().__init__(*args, **kwargs)

    async def detail_one_parse(self, data, company_name, company_id):
        """
        单独解析一个tr
        :return:
        """
        data = json.loads(data)
        rules = ('result', 'announcement', 'objection')
        kwargs = {'company_name': company_name, 'company_id': company_id}
        [kwargs.update(data.get(rule)) for rule in rules]
        kwargs.update({'total': data.get('total')})

        tup = ('brief_cancel_result', 'reg_authority', 'credit_code', 'announcement_term', 'announcement_end_date',
               'ossPath', 'objection_content', 'objection_date', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_brief_cancel {keys} value {values};'
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
            trs = self.get_xpath('//script[@id="brief_cancel_announcements_data"]//text()', response=resp.text)
            async with aiohttp.ClientSession() as session:
                await asyncio.gather(*[self.detail_one_parse(data, company_name, company_id) for data in trs])
        except Exception as e:
            print(f'类 - - {BriefCancel.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
