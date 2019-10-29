import pymysql
import hashlib

INFO = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'qwe123',
    'db': 'chanyeyuan',
    'charset': 'utf8'
}

INSERT_INFO = {
    'host': '221.214.181.70',
    'port': 33061,
    'user': 'uniccc',
    'db': 'uniccc_python',
    'password': 'Uniccc2019@db',
    'charset': 'utf8'
}

info = {
    "11":"北京市",
    "10":"北京市",
    "12":"天津市",
    "13":"河北省",
    "14":"山西省",
    "15":"内蒙古自治区",
    "21":"辽宁省",
    "22":"吉林省",
    "23":"黑龙江省",
    "31":"上海市",
    "32":"江苏省",
    "33":"浙江省",
    "34":"安徽省",
    "35":"福建省",
    "36":"江西省",
    "37":"山东省",
    "41":"河南省",
    "42":"湖北省",
    "43":"湖南省",
    "44":"广东省",
    "45":"广西壮族自治区",
    "46":"海南省",
    "51":"四川省",
    "52":"贵州省",
    "50":"重庆市",
    "53":"云南省",
    "54":"西藏自治区",
    "61":"陕西省",
    "62":"甘肃省",
    "63":"青海省",
    "64":"宁夏回族自治区",
    "65":"新疆维吾尔自治区",
    "71":"台湾省",
    "81":"香港特别行政区",
    "82":"澳门特别行政区"
}


class SaveMysql(object):
    def __init__(self):
        self.connection1 = pymysql.connect(**INFO)
        self.cur1 = self.connection1.cursor()
        self.connection2 = pymysql.connect(**INSERT_INFO)
        self.cur2 = self.connection2.cursor()

    @property
    def _get_mysql_data_count(self):
        """
        获取mysql总数
        :return:
        """
        try:
            self.cur1.execute('select count(col_id) from company_basc_info;')
            count = int(self.cur1.fetchone()[0])
        except:
            self.cur1.execute('select count(col_id) from company_basc_info;')
            count = int(self.cur1.fetchone()[0])

        return count

    def get_md5_key(self, company_name):
        hash = hashlib.md5(company_name.encode())
        return hash.hexdigest()

    def get_company_name(self, id):
        """
        获取对应id的企业，自增id
        :param id:
        :return:
        """
        try:
            self.cur1.execute(f'select entName from company_basc_info where col_id={id};')
            result = self.cur1.fetchone()
            company_name = result[0]
            md5_key = self.get_md5_key(company_name)
            return md5_key, company_name

        except Exception as e:
            self.connection1.rollback()

    def save_to_other_db(self, company_name, md5_key):
        try:
            self.cur2.execute(f'insert into das_tm_company_info (md5Key, companyName) value ("{md5_key}", "{company_name}")')
            self.connection2.commit()
            print('ok')
        except:
            self.connection2.rollback()

    def run(self):
        count = self._get_mysql_data_count
        for i in range(1, count+1):
            md5_key, company_name = self.get_company_name(i)
            print(md5_key, company_name)
            self.save_to_other_db(company_name, md5_key)

# =================================================================================================================================
    def save_province(self, reg_no, company_name):
        try:
            province = info.get(reg_no)
            self.cur2.execute(f'update das_tm_company_info set companyProvince="{province}" where companyName = "{company_name}";')
            self.connection2.commit()
            # print(province)
            print('ok')
        except:
            self.connection2.rollback()

    def save_one_province(self, reg_no, company_name):
        try:
            if reg_no == '12':
                self.cur2.execute(f'update das_tm_company_info set companyProvince="{"天津市"}" where companyName = "{company_name}";')
                self.connection2.commit()
                print('ok')
            else:
                print('no')

        except:
            self.connection2.rollback()

    def get_reg_and_company(self, id):
        try:
            self.cur1.execute(f'select creditCode, entName from company_basc_info where col_id={id};')
            result = self.cur1.fetchone()
            reg_no = result[0][2:4]
            company_name = result[1]
            return reg_no, company_name

        except Exception as e:
            self.connection1.rollback()

    def run_province(self):
        count = self._get_mysql_data_count
        for i in range(1, count+1):
            reg_no, company_name = self.get_reg_and_company(i)
            self.save_province(reg_no, company_name)


if __name__ == '__main__':
    s = SaveMysql()
    s.run_province()