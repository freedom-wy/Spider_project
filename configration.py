from Dimension_spider.basic_information.main_staff_spider import MainStaffSpider
from Dimension_spider.basic_information.foreign_investment_spider import ForeignInvestmentSpider
from Dimension_spider.basic_information.shareholder_info_spider import ShareholderInfoSpider
from Dimension_spider.listing_information.stock_quotation_spider import StockQuotation
from Dimension_spider.listing_information.company_profile_spider import CompanyProfile
from Dimension_spider.listing_information.security_spider import Security
from Dimension_spider.listing_information.primary_indicator_spider import PrimaryIndicator
from Dimension_spider.listing_information.corp_basic_spider import CorpBasic
from Dimension_spider.listing_information.corp_contact_spider import CorpContact
from Dimension_spider.listing_information.senior_executive import SeniorExecutive
from Dimension_spider.listing_information.share_holder_spider import ShareHolder
from Dimension_spider.listing_information.issue_related_spider import IssueRelated
from Dimension_spider.listing_information.share_structure_spider import ShareStructure
from Dimension_spider.operating_conditions.bids_info_spider import BidsInfo
from Dimension_spider.listing_information.announcement_spider import Announcement
from Dimension_spider.basic_information.human_holding_spider import HumanHolding
from Dimension_spider.basic_information.branch_organization import BranchOrganization
from Dimension_spider.basic_information.change_info_spider import ChangeInfo
from Dimension_spider.basic_information.company_public_spider import CompanyPublic
from Dimension_spider.basic_information.holder_change_spider import HolderChange
from Dimension_spider.judicial_risk.ktannouncement_spider import KtannouncementSpider
from Dimension_spider.judicial_risk.law_suit_spider import LawSuit
from Dimension_spider.judicial_risk.executor_info_spider import ExecutorInfo
from Dimension_spider.judicial_risk.send_announcement_spider import SendAnnouncement
from Dimension_spider.judicial_risk.court_register_spider import CourtRegister
from Dimension_spider.listing_information.illegal_processing_spider import IllegalProcessing
from Dimension_spider.judicial_risk.judicial_assistance_spider import JudicialAssistance
from Dimension_spider.business_risk.abnormal_info_spider import AbnormmalInfo
from Dimension_spider.business_risk.illegal_remove_spider import IllegalRemove
from Dimension_spider.business_risk.illegal_put_spider import IllegalPut
from Dimension_spider.business_risk.puni_shment_spider import PuniShment
from Dimension_spider.business_risk.credit_china_spider import CreditChina
from Dimension_spider.business_risk.environmental_penalty_spider import EnvironmentalPenalty
from Dimension_spider.business_risk.mortgage_info_spider import MortgageInfo
from Dimension_spider.business_risk.equity_info_spider import EquityInfo
from Dimension_spider.business_risk.land_mortgage_spider import LandMortgage
from Dimension_spider.business_risk.intellectual_property_spider import IntellectualProperty
from Dimension_spider.business_risk.taxation_offences_details_spider import TaxationOffences
from Dimension_spider.business_risk.own_tax_spider import OwnTax
from Dimension_spider.business_risk.judicial_sale_spider import JudicialSale
from Dimension_spider.business_risk.public_notice_spider import PublicNotice
from Dimension_spider.business_risk.liquidating_info_spider import LiquidatingInfo
from Dimension_spider.business_risk.brief_cancel_spider import BriefCancel
from Dimension_spider.operating_conditions.administration_license_spider import AdministrationLicense
from Dimension_spider.operating_conditions.administration_license_china_spider import AdministrationLicenseChina
from Dimension_spider.operating_conditions.tax_credit_spider import TaxCredit
from Dimension_spider.operating_conditions.employments_spider import Employments
from Dimension_spider.operating_conditions.spot_check_spider import SpotCheck
from Dimension_spider.operating_conditions.import_and_export_spider import ImportAndExport
from Dimension_spider.operating_conditions.certificate_spider import Certificate
from Dimension_spider.operating_conditions.purchase_land_spider import PurchaseLand
from Dimension_spider.operating_conditions.land_publicity_spider import LandPublicity
from Dimension_spider.operating_conditions.land_transfer_spider import LandTransfer
from Dimension_spider.operating_conditions.bond_details_spider import BondDetails


# 配置文件

# 实例每个爬虫
# 主要人员爬虫
main = MainStaffSpider()
# 对外投资爬虫
annual = ForeignInvestmentSpider()
# 股东信息爬虫
shareholder = ShareholderInfoSpider()
# 股票行情爬虫
stock = StockQuotation()
# 公司简介爬虫
company = CompanyProfile()
# 证券信息爬虫
security = Security()
# 主要指标爬虫
primary = PrimaryIndicator()
# 重要人员爬虫
corp = CorpBasic()
# 联系信息爬虫
contact = CorpContact()
# 高管信息爬虫
senior = SeniorExecutive()
# 十大股东爬虫
share = ShareHolder()
# 发行相关爬虫
issue = IssueRelated()
# 股本结构爬虫
structure = ShareStructure()
# 招投标爬虫
bids = BidsInfo()
# 上市公告爬虫
announce = Announcement()
# 最终受益人爬虫
human = HumanHolding(cookie='vip')
# 分支机构爬虫
branch = BranchOrganization()
# 变更记录爬虫
change = ChangeInfo()
# 股东及出资信息爬虫（公司公示）
public = CompanyPublic()
# 股权变更信息爬虫（公司公示）
holder = HolderChange()
# 开庭公告爬虫
kt = KtannouncementSpider()
# 法律诉讼爬虫
law = LawSuit()
# 被执行人爬虫
executor = ExecutorInfo()
# 送达公告爬虫
send = SendAnnouncement()
# 立案信息爬虫
court = CourtRegister()
# 违规处理爬虫
illegal = IllegalProcessing()
# 司法协助爬虫
judicial = JudicialAssistance()
# 经营异常爬虫
abnormal = AbnormmalInfo()
# 严重违法（移出）
remove = IllegalRemove()
# 严重违法（列入）
put = IllegalPut()
# 行政处罚（工商局）
punishment = PuniShment()
# 行政处罚（信用中国）
credit = CreditChina()
# 环保处罚爬虫
environmental = EnvironmentalPenalty()
# 动产抵押爬虫
mortgage = MortgageInfo()
# 股权出质爬虫
equity = EquityInfo()
# 土地抵押爬虫
land = LandMortgage()
# 知识产权出质爬虫
intellectual = IntellectualProperty()
# 税收违法详情爬虫
taxation = TaxationOffences()
# 欠税公告爬虫
own = OwnTax()
# 司法拍卖爬虫
sale = JudicialSale()
# 公示催告爬虫
notice = PublicNotice()
# 清算信息爬虫
liquidate = LiquidatingInfo()
# 简易注销爬虫
brief = BriefCancel()
# 行政许可（工商局）爬虫
admin = AdministrationLicense()
# 行政许可（信用中国）爬虫
admin_china = AdministrationLicenseChina()
# 税务评级爬虫
tax = TaxCredit()
# 招聘信息爬虫
employ = Employments()
# 抽查检查爬虫
spot = SpotCheck()
# 进出口信用爬虫
export = ImportAndExport()
# 资质证书爬虫
certificate = Certificate()
# 购地信息爬虫
purchase = PurchaseLand()
# 地块公示爬虫
land_publicity = LandPublicity()
# 土地转让爬虫
transfer = LandTransfer()
# 证券信息爬虫
bond = BondDetails()

# 维度列表
CLASS_LIST = [
    # 主要人员
    # '_container_staff',
    # # 对外投资,
    # '_container_invest',
    # # 股东信息
    # '_container_holder',
    # 股票行情
    # '_container_volatilityNum',
    # 企业简介爬虫
    # 'nav-main-stockNum',
    # 证券信息爬虫
    # '_container_secBasicInfo',
    # 主要指标爬虫
    # '_container_corpMainIndex',
    # 重要人员爬虫
    # '_container_corpBasicInfo',
    # 联系信息爬虫
    # '_container_corpContactInfo',
    # 高管信息爬虫
    # '_container_seniorPeople',
    # 十大股东爬虫
    # '_container_topTenNum',
    # 发行相关爬虫
    # 'nav-main-issueRelatedNum',
    # 股本结构爬虫
    # '_container_shareStructure',
    # 招投标爬虫
    # '_container_bid',
    # 上市公告爬虫
    # '_container_announcement',
    # 最终受益人爬虫 vip
    # '_container_humanholding',
    # 分支机构爬虫
    # '_container_branch',
    # 变更记录爬虫
    # '_container_changeinfo',
    # 股东及出资信息爬虫（公司公示）
    # '_container_holderList',
    # 股权变更信息爬虫（公司公示）
    # '_container_stockChangeInfo',
    # 开庭公告爬虫
    # '_container_announcementcourt',
    # 法律诉讼爬虫
    # '_container_lawsuit'
    # 被执行人爬虫
    # '_container_zhixing',
    # 送达公告爬虫
    # '_container_sendAnnouncements',
    # 立案信息爬虫
    # '_container_courtRegister',
    # 违规处理爬虫
    # '_container_corpIllegals',
    # 司法协助爬虫
    # '_container_judicialAid',
    # 经营异常爬虫
    # '_container_abnormalRemove',
    # 严重违法爬虫（移出）
    # '_container_illegalRemove',
    # 严重违法爬虫（列入）
    # '_container_illegalPut',
    # 行政处罚爬虫（工商局）
    # '_container_punish',
    # 行政处罚爬虫（信用中国）
    # '_container_punishmentCreditchina',
    # 环保处罚爬虫
    # '_container_environmentalPenalties',
    # 动产抵押爬虫
    # '_container_mortgage',
    # 股权出质爬虫
    # '_container_equity',
    # 土地抵押爬虫
    # '_container_landMortgages',
    # 知识产权出质爬虫
    # '_container_intellectualProperty',
    # 税收违法详情爬虫
    # '_container_taxContraventions',
    # 欠税公告爬虫
    # '_container_towntax',
    # 司法拍卖爬虫
    # '_container_judicialSale',
    # 公示催告爬虫
    # '_container_publicnoticeItem',
    #  清算信息爬虫
    # '_container_clearingCount',
    # 简易注销爬虫
    # '_container_briefCancelAnnouncements'
    # 行政许可（工商局）爬虫
    # '_container_licensing',
    # 行政许可（信用中国）爬虫
    # '_container_licensingXyzg',
    # 税务评级爬虫
    # '_container_taxcredit',
    # 招聘信息爬虫
    # '_container_baipin',
    # 抽查检查爬虫
    # '_container_check',
    # 进出口信用爬虫
    # '_container_importAndExport',
    # 资质证书爬虫
    # '_container_certificate',
    # 购地信息爬虫
    # '_container_purchaselandV2',
    # 地块公示爬虫
    # '_container_landPublicitys',
    # 土地转让爬虫
    # '_container_landTransfers',
    # 证券信息爬虫
    '_container_bond',

]

CLASS_INFO_DICT = {
    'company_name': None,
    'company_id': None,
    'data': {
        # 主要人员
        '_container_staff': {
            'func': main,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_staff"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 对外投资
        '_container_invest': {
            'func': annual,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_invest"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 股东信息
        '_container_holder': {
            'func': shareholder,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_holder"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 股票行情
        '_container_volatilityNum': {
            'func': stock,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_volatilityNum"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 公司简介
        'nav-main-stockNum': {
            'func': company,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="nav-main-stockNum"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 证券信息爬虫
        '_container_secBasicInfo': {
            'func': security,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_secBasicInfo"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 主要指标爬虫
        '_container_corpMainIndex': {
            'func': primary,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_corpMainIndex"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 重要人员爬虫
        '_container_corpBasicInfo': {
            'func': corp,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_corpBasicInfo"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 联系信息爬虫
        '_container_corpContactInfo': {
            'func': contact,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_corpBasicInfo"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 高管信息爬虫
        '_container_seniorPeople': {
            'func': senior,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_seniorPeople"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 十大股东爬虫
        '_container_topTenNum': {
            'func': share,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_topTenNum"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 发行相关爬虫
        'nav-main-issueRelatedNum': {
            'func': issue,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_topTenNum"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 股本结构爬虫
        '_container_shareStructure': {
            'func': structure,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_shareStructure"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 股本结构爬虫
        '_container_bid': {
            'func': bids,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_bid"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 上市公告爬虫
        '_container_announcement': {
            'func': announce,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_announcement"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 最终受益人爬虫
        '_container_humanholding': {
            'func': human,
            'total_num': None,
            'one_page': 20,
            'total_num_xpath': '//div[@id="_container_humanholding"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 分支机构爬虫
        '_container_branch': {
            'func': branch,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_branch"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 变更记录爬虫爬虫
        '_container_changeinfo': {
            'func': change,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_changeinfo"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 股东及出资信息爬虫（公司公示）
        '_container_holderList': {
            'func': public,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_holderList"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 股权变更信息爬虫（公司公示）
        '_container_stockChangeInfo': {
            'func': holder,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_stockChangeInfo"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 开庭公告爬虫
        '_container_announcementcourt': {
            'func': kt,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_announcementcourt"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 法律诉讼爬虫
        '_container_lawsuit': {
            'func': law,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_lawsuit"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 被执行人爬虫
        '_container_zhixing': {
            'func': executor,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_zhixing"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 送达公告爬虫
        '_container_sendAnnouncements': {
            'func': send,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_sendAnnouncements"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 立案信息爬虫
        '_container_courtRegister': {
            'func': court,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_courtRegister"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 违规处理爬虫
        '_container_corpIllegals': {
            'func': illegal,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_corpIllegals"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 司法协助爬虫
        '_container_judicialAid': {
            'func': judicial,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_judicialAid"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 经营异常爬虫
        '_container_abnormalRemove': {
            'func': abnormal,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_abnormalRemove"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 严重违法爬虫（移出）
        '_container_illegalRemove': {
            'func': remove,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_illegalRemove"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 严重违法爬虫（列入）
        '_container_illegalPut': {
            'func': put,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_illegalPut"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 行政处罚爬虫（工商局）
        '_container_punish': {
            'func': punishment,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_punish"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 行政处罚爬虫（信用中国）
        '_container_punishmentCreditchina': {
            'func': credit,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_punishmentCreditchina"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 环保处罚爬虫
        '_container_environmentalPenalties': {
            'func': environmental,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_environmentalPenalties"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 动产抵押爬虫
        '_container_mortgage': {
            'func': mortgage,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_mortgage"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 股权出质爬虫
        '_container_equity': {
            'func': equity,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_equity"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 土地抵押爬虫
        '_container_landMortgages': {
            'func': land,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_landMortgages"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 知识产权出质爬虫
        '_container_intellectualProperty': {
            'func': intellectual,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_intellectualProperty"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 税收违法爬虫
        '_container_taxContraventions': {
            'func': taxation,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_taxContraventions"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 欠税公告爬虫
        '_container_towntax': {
            'func': own,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_towntax"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 司法拍卖爬虫
        '_container_judicialSale': {
            'func': sale,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_judicialSale"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 公示催告爬虫
        '_container_publicnoticeItem': {
            'func': notice,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_publicnoticeItem"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 清算信息爬虫
        '_container_clearingCount': {
            'func': liquidate,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_clearingCount"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 简易注销爬虫
        '_container_briefCancelAnnouncements': {
            'func': brief,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_briefCancelAnnouncements"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 行政许可（工商信息）爬虫
        '_container_licensing': {
            'func': admin,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_licensing"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 行政许可（信用中国）爬虫
        '_container_licensingXyzg': {
            'func': admin_china,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_licensingXyzg"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 税务评级爬虫
        '_container_taxcredit': {
            'func': tax,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_taxcredit"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 招聘信息爬虫
        '_container_baipin': {
            'func': employ,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_baipin"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 抽查检查爬虫
        '_container_check': {
            'func': spot,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_check"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 进出口信用爬虫
        '_container_importAndExport': {
            'func': export,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_importAndExport"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 资质证书爬虫
        '_container_certificate': {
            'func': certificate,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_certificate"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 购地信息爬虫
        '_container_purchaselandV2': {
            'func': purchase,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_purchaselandV2"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 地块公示爬虫
        '_container_landPublicitys': {
            'func': land_publicity,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_landPublicitys"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },
        # 土地转让爬虫
        '_container_landTransfers': {
            'func': transfer,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_landTransfers"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'coroutine',
        },
        # 债券信息爬虫
        '_container_bond': {
            'func': bond,
            'total_num': None,
            'one_page': 10,
            'total_num_xpath': '//div[@id="_container_bond"]//ul[@class="pagination"]/@page-total',
            'response': None,
            'status': 'async',
        },


    }
}

# UA
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 数据库配置
MYSQL_INFO = {
    'host': '221.214.181.70',
    'port': 33061,
    'user': 'uniccc',
    'db': 'uniccc_python',
    'password': 'Uniccc2019@db',
    'charset': 'utf8'
}
