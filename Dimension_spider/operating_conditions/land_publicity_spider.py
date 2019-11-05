import json

import re
import aiohttp
import asyncio

from utils.Base_spider import BaseSpider


class LandPublicity(BaseSpider):
    """
    地块公示爬虫
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
        # 发布日期
        publication_date = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 地块位置
        land_location = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 行政区
        administrative_district = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 土地面积
        land_area = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 土地用途
        land_usefulness = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 发布机关
        publication_organize = ''.join(self.get_xpath('./td[7]//text()', html=tr))
        # id
        info = ''.join(self.get_xpath('./td[8]/span/@onclick', html=tr))
        zid = ''.join(re.findall(r'openLandPublicityDetail\("(.*?)"\)', info, re.S))
        kwargs.update({
            'publication_date': publication_date,
            'land_location': land_location,
            'administrative_district': administrative_district,
            'land_area': land_area,
            'land_usefulness': land_usefulness,
            'publication_organize': publication_organize,
            'details_id': int(zid),
        })

        tup = ('publication_organize', 'land_usefulness', 'administrative_district', 'land_location',
               'publication_date', 'land_area', 'company_name', 'company_id', 'details_id')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_land_publicity_info {keys} value {values};'
        print(sql)
        self.operating.save_mysql(sql)
        url = f'https://www.tianyancha.com/company/getLandPublicityDetail.json?id={zid}&_={self.get_now_timestamp()}'
        async with session.get(url, headers=self.set_x_auth_token) as resp:
            result = await resp.json()
            data = result.get('data')
            data.update({'landUser_clean': json.dumps(data.get('landUser_clean')),
                         'landUser_clean_app': json.dumps(data.get('landUser_clean_app')), 'id': int(zid)})

            tup = ('id', 'landUser_clean', 'publication_organize', 'contact_person', 'land_location', 'land_area', 'remark',
                   'public_announcement_period', 'land_num', 'project_name', 'contact_number', 'electronic_mail',
                   'organize_location', 'land_usefulness', 'feedback_method', 'publication_date', 'contact_organize',
                   'postal_code', 'landUser_clean_app')
            values, keys = self.structure_sql_statement(tup, data)
            sql = f'insert into das_tm_land_publicity_details {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/landPublicitys.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.get_headers) as resp:
                    response = await resp.text() if await resp.text() else '<div></div>'
                    trs = self.get_xpath('//table[@class="table"]/tbody/tr', response=response)
                    if trs:
                        await asyncio.gather(
                            *[self.detail_one_parse(tr, company_name, company_id, session) for tr in trs])
                    else:
                        print('数据为空')
        except Exception as e:
            print(f'类 - - {LandPublicity.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
