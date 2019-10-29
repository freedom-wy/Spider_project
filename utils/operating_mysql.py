import pymysql

# 数据库配置
MYSQL_INFO = {
    'host': '221.214.181.70',
    'port': 33061,
    'user': 'uniccc',
    'db': 'uniccc_python',
    'password': 'Uniccc2019@db',
    'charset': 'utf8'
}


class OperatingMysql(object):
    """
    操作mysql
    """
    def __init__(self):
        self.connection = pymysql.connect(**MYSQL_INFO)
        self.cursor = self.connection.cursor()

    def save_mysql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print('插入成功 - - commit')
        except:
            self.connection.rollback()
            print('插入失败 - - rollback')

if __name__ == '__main__':
    pass