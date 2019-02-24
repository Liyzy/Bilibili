import codecs
import csv
import pymysql

conn = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1217",
    "database": "bilibili",
    "charset": "utf8mb4"
}

db = pymysql.connect(**conn)
cursor = db.cursor()


def create_db():
    # 创建数据库
    global cursor
    cursor.execute("""create table if not exists video_info_from_web
                   (v_aid int primary key,
                    v_view int,
                    v_danmaku int,
                    v_reply int,
                    v_favorite int,
                    v_coin int,
                    v_share int)""")


def insert(cur, sql, args):
    try:
        cur.execute(sql, args)
    except Exception as e:
        print(e)
        db.rollback()


# 将csv文件数据导入到mysql中
def read_csv_to_mysql(filename):
    global cursor, db
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        sql = 'insert into video_info_from_web values(%s,%s,%s,%s,%s,%s,%s)'
        for item in reader:
            if item[1] is None or item[1] == '':
                continue
            args = tuple(item)
            insert(cursor, sql=sql, args=args)

        db.commit()
        cursor.close()
        db.close()


if __name__ == '__main__':
    read_csv_to_mysql(r"D:\thunder\result.csv")
