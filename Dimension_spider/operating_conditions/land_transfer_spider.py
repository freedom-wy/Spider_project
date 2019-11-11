import re
import json

from utils.Base_spider import BaseSpider


class LandTransfer(BaseSpider):
    """
    土地转让爬虫
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
        # id
        info = ''.join(self.get_xpath('./td[8]/span/@onclick', html=tr))
        zid = ''.join(re.findall(r'openLandTransferDetail\((.*?)\)', info, re.S))
        url = f'https://www.tianyancha.com/company/getLandTransferDetail.json?id={zid}&_={self.get_now_timestamp()}'
        kwargs = self.download(url, headers=self.set_x_auth_token).json().get('data')
        kwargs.update({'user_change_now_clean_app': json.dumps(kwargs.get('user_change_now_clean_app')),
                     'user_change_pre_clean_app': json.dumps(kwargs.get('user_change_pre_clean_app')),
                       'company_name': company_name,
                       'company_id': company_id})

        tup = ('area', 'merchandise_time', 'years_of_use', 'level', 'num', 'aministrativeArea', 'user_change_pre_clean_app',
               'merchandise_price', 'use_type', 'user_change_now_clean_app', 'location', 'useful', 'merchandise_type',
               'mark', 'situation', 'company_name', 'company_id', 'user_change_pre_clean', 'user_change_now_clean')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_land_transfer_info {keys} value {values};'
        print(sql)
        self.operating.save_mysql(sql)

    def parse(self, company_id, company_name, ps=20, pn=1, resp=None):
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
            result = self.download(
                f'https://www.tianyancha.com/pagination/landTransfers.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}')
            trs = self.get_xpath('//table[@class="table -breakall"]/tbody/tr', response=result.text)
            for tr in trs:
                self.detail_one_parse(tr, company_name, company_id)

        except Exception as e:
            print(f'类 - - {LandTransfer.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
