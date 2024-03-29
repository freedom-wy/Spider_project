import aiohttp
import asyncio

from utils.Base_spider import BaseSpider


class HolderChange(BaseSpider):
    """
    股权变更信息（公司公示）
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
        # 股东发起人
        name = ''.join(self.get_xpath('./td[2]//td[2]//text()', html=tr))
        # 变更后
        ratio_after = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 变更前
        ratio_before = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 变更时间
        change_time = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # logo
        logo = ''.join(self.get_xpath('./td[2]//td[1]//img/@data-src', html=tr))

        kwargs = {
            'name': name,
            'ratio_after': ratio_after,
            'ratio_before': ratio_before,
            'change_time': change_time,
            'logo': logo,
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('company_name', 'company_id', 'name', 'ratio_after', 'logo', 'ratio_before',
               'type', 'change_time')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_holder_change_info {keys} value {values};'
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
        #     f'https://www.tianyancha.com/pagination/stockChangeInfo.xhtml?ps={ps}0&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
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
            url = f'https://www.tianyancha.com/pagination/stockChangeInfo.xhtml?ps={ps}0&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('数据为空')
        except Exception as e:
            print(f'类 - - {HolderChange.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
