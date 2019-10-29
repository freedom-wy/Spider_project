# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TycProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    approved_time = scrapy.Field()  # 核准时间
    business_scope = scrapy.Field()  # 经营范围
    company_id = scrapy.Field()  # 企业id
    company_name = scrapy.Field()  # 企业名
    company_org_type = scrapy.Field()  # 企业类型
    credit_code = scrapy.Field()  # 社会统一信用代码
    estiblish_time = scrapy.Field()  # 成立日期
    history_names = scrapy.Field()  # 曾用名
    industry = scrapy.Field()  # 行业
    operating_period = scrapy.Field()  # 营业期限
    org_number = scrapy.Field()  # 组织机构代码
    property3 = scrapy.Field()  # 英文名
    reg_capital = scrapy.Field()  # 注册资本
    reg_institute = scrapy.Field()  # 登记机关
    reg_location = scrapy.Field()  # 注册地址
    reg_number = scrapy.Field()  # 注册号
    reg_status = scrapy.Field()  # 企业状态
    social_staff_num = scrapy.Field()  # 参保人数
    source = scrapy.Field()  # 来源
    staff_num_range = scrapy.Field()  # 人员规模
    tax_number = scrapy.Field()  # 纳税人识别号
    actual_capital = scrapy.Field()  # 实缴资本
    tax_payer = scrapy.Field()  # 纳税人资质
