import asyncio
import aiohttp

from utils.Base_spider import BaseSpider


class CopyRegWorks(BaseSpider):
    """
    作品著作权爬虫
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
        # 作品名称
        fullname = ''.join(self.get_xpath('./td[2]//text()', html=tr))
        # 登记号
        regnum = ''.join(self.get_xpath('./td[3]//text()', html=tr))
        # 作品类别
        type = ''.join(self.get_xpath('./td[4]//text()', html=tr))
        # 创作完成日期
        finishTime = ''.join(self.get_xpath('./td[5]//text()', html=tr))
        # 登记日期
        regtime = ''.join(self.get_xpath('./td[6]//text()', html=tr))
        # 首次发表日期
        publishtime = ''.join(self.get_xpath('./td[7]//text()', html=tr))

        kwargs = {
            'fullname': fullname,
            'regnum': regnum,
            'type': type,
            'finishTime': finishTime,
            'regtime': regtime,
            'publishtime': publishtime,
            'company_name': company_name,
            'company_id': company_id
        }
        tup = ('regtime', 'authorNationality', 'publishtime', 'finishTime', 'type', 'fullname',
               'company_name', 'company_id', 'regnum')
        values, keys = self.structure_sql_statement(tup, kwargs)
        sql = f'insert into das_tm_copy_reg_works_info {keys} value {values};'
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
            url = f'https://www.tianyancha.com/pagination/copyrightWorks.xhtml?ps={ps}&pn={pn}&id={company_id}&_={self.get_now_timestamp()}'
            resp = self.download(url)
            response = resp.text if resp else '<div></div>'
            trs = self.get_xpath('//table[@class="table -sort"]/tbody/tr', response=response)
            if trs:
                for tr in trs:
                    self.detail_one_parse(tr, company_name, company_id)
            else:
                print('无数据')

        except Exception as e:
            print(f'类 - - {CopyRegWorks.__name__} - - 异步请求出错：', e)


if __name__ == '__main__':
    pass
