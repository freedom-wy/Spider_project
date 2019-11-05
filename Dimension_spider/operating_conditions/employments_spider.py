import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class Employments(BaseSpider):
    """
    招聘信息爬虫
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
        # 发布日期
        startdate = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 招聘职位
        title = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 月薪
        oriSalary = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 学历
        education = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 工作经验
        experience = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 地区
        city = ''.join(self.get_xpath('./td[7]//text()', html=tr))
        # url
        webInfoPath = ''.join(self.get_xpath('./td[8]/a/@href', html=tr))

        kwargs = {
            'startdate': startdate,
            'title': title,
            'oriSalary': oriSalary,
            'education': education,
            'experience': experience,
            'city': city,
            'webInfoPath': webInfoPath,
            'company_name': company_name,
            'company_id': company_id
        }

        tup = ('education', 'city', 'webInfoPath', 'source', 'title', 'experience', 'startdate', 'welfare',
               'oriSalary', 'company_name', 'company_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_employments_info {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/baipin.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(*[self.detail_one_parse(tr, company_name, company_id) for tr in trs])
                    else:
                        print('无数据')

        except Exception as e:
            print(f'类 - - {Employments.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
