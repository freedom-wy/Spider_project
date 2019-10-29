import pymysql
from xlsxwriter import Workbook


INFO = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'qwe123',
    'db': 'chanyeyuan',
    'charset': 'utf8'
}

connection = pymysql.connect(**INFO)
cur = connection.cursor()
cur.execute("SELECT entName, creditCode, regNo, frName FROM `company_basc_info` WHERE entName like '烟台%';")
data = cur.fetchall()
# for i in cur.fetchall():
#     print(i)

def sheet_w(data=None):
    ws = Workbook('python_send.xlsx')
    wb = ws.add_worksheet('Sheet1')

    # 构造表格属性
    STYLE_HEADER = {'font_size': 9, 'border': 1, 'bold': 1, 'bg_color': '#B4C6E7', 'align': 'center',
                    'valign': 'vcenter'}
    STYLE_TEXT = {'font_size': 9, 'border': 1}
    STYLE_NUMBER = {'font_size': 9, 'border': 1, 'num_format': '0.00'}

    # 设置表格属性
    style_header = ws.add_format(STYLE_HEADER)
    style_text = ws.add_format(STYLE_TEXT)
    style_number = ws.add_format(STYLE_NUMBER)

    # 添加表头
    header = ["公司名", "社会统一信用代码", "工商注册号", "法定代表人"]
    # 在第一行设置表头
    wb.write_row('A1', header, style_header)

    # 宽度
    widths = [8, 15, 15, 15]
    # 设置宽度
    for ind, wid in enumerate(widths):
        # print(ind, wid)
        wb.set_column(ind, ind, wid)

    for ind, data in enumerate(data):
        # ind+1 表示第几行， 第二个参数是第几列， 第三个参数是值， 第四个参数是属性
        wb.write(ind + 1, 0, data[0], style_text)
        wb.write(ind + 1, 1, data[1], style_number)
        wb.write(ind + 1, 2, data[2], style_number)
        wb.write(ind + 1, 3, data[3], style_text)
        # 添加完成就关闭
    ws.close()

sheet_w(data)

# if __name__ == '__main__':
#     sheet_w()

