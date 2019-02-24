import pymysql
from pyecharts import Pie

conn = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1217",
    "database": "bilibili",
    "charset": "utf8mb4"
}

db = pymysql.connect(**conn)
print("Database has connected!")
cursor = db.cursor()


def get_total_number():
    global cursor
    sql = 'select count(*) from user_info where sex is not null'
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]
    except:
        db.rollback()


def get_sex_info(sex):
    global cursor
    sql = 'select count(*) from user_info where sex=%s'
    try:
        cursor.execute(sql, sex)
        result = cursor.fetchone()
        return result[0]
    except:
        db.rollback()


def sex_ratio_visualization(columns, ratio):
    pie = Pie("B站性别占比饼状图", "2018-12-31", width=900, height=700)
    pie.add("性别占比", columns, ratio, title_pos='center',
            legend_top='bottom', is_legend_show=True, is_label_show=True)
    pie.render(r'sex_ratio.html')


if __name__ == "__main__":
    total_number = get_total_number()
    male = get_sex_info('男')/total_number
    female = get_sex_info('女')/total_number
    secrecy = get_sex_info('保密')/total_number
    col = ['男', '女', '保密']
    sex_ratio = [male, female, secrecy]
    sex_ratio_visualization(col, sex_ratio)
    print(male, female, secrecy)
    print("Done!!!")
