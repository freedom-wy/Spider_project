# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .settings import INSERT_INFO
from .send_email import SendEmail


class TycProjectPipeline(object):

    def open_spider(self, spider):
        self.connection = pymysql.connect(**INSERT_INFO)
        self.cur = self.connection.cursor()
        self.email = SendEmail()

    def process_item(self, item, spider):
        """
        存入数据库
        :param item:
        :param spider:
        :return:
        """
        try:
            keys = list()
            values = list()
            for key, value in item.items():
                keys.append(key)
                values.append(value)
            sql = f"INSERT INTO das_tm_base_info {tuple(keys)}".replace("'", "")
            self.cur.execute(f"{sql} value {tuple(values)}")
            self.connection.commit()
            # print(f"INSERT INTO das_tm_base_info {tuple(keys)} value {tuple(values)}")

        except Exception:
            self.connection.rollback()
        return item

    def close_spider(self, spider):
        self.email.run('The spider has stopped You look at it!')
        self.cur.close()
        self.connection.close()
