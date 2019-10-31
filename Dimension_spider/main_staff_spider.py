import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class MainStaffSpider(BaseSpider):
    """
    主要人员爬虫
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
        name = ''.join(self.get_xpath('./td[2]//td[2]//text()', html=tr))
        # 主要人员职务
        typejoin = '-'.join(self.get_xpath('./td[3]//text()', html=tr))
        # 主要人员图片
        logo = ''.join(self.get_xpath('./td[2]//td[1]//img[@class="img"]/@data-src', html=tr))

        kwargs = {
            'logo': logo,
            'name': name,
            'company_name': company_name,
            'company_id': company_id,
            'typeJoin': typejoin
        }
        tup = ('logo', 'type', 'name', 'company_name', 'typeJoin', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_staff_info {keys} value {values};'
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
        # resp = self.download(f'https://www.tianyancha.com/pagination/staff.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
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
            url = f'https://www.tianyancha.com/pagination/staff.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')
        except Exception as e:
            print(f'类 - - {MainStaffSpider.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    main = MainStaffSpider()
    main.run('1', '2', 22, 20, '')