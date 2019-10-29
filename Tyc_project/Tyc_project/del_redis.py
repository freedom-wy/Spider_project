import redis
import pymysql


INSERT_INFO = {
    'host': '221.214.181.70',
    'port': 33061,
    'user': 'uniccc',
    'db': 'uniccc_python',
    'password': 'Uniccc2019@db',
    'charset': 'utf8'
}

INFO = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'qwe123',
    'db': 'chanyeyuan',
    'charset': 'utf8'
}


connection2 = pymysql.connect(**INFO)
cursor2 = connection2.cursor()


connection = pymysql.connect(**INSERT_INFO)
cursor = connection.cursor()

