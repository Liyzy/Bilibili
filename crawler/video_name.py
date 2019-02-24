import pymysql
import requests
import pyquery

conn = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1217",
    "database": "bilibili",
    "charset": "utf8mb4"
}

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
}

db = pymysql.connect(**conn)
print("Database has connected. Get names...")
cursor = db.cursor()


def get_video_aid():
    global cursor
    sql = "select v_aid from video_info where v_name=\"\""
    cursor.execute(sql)
    for _aid in cursor.fetchall():
        yield _aid[0]


def get_video_name(aids):
    url = "https://www.bilibili.com/video/av{}"
    for i in aids:
        try:
            req = requests.get(url.format(i), headers=headers).text
            q = pyquery.PyQuery(req)
            # title = q('title').text()  # 这样得到的结果带有其他信息，如标签、B站logo等
            # title = title[0: title.find('_')]  # 去掉原title中的其他信息
            yield {i: q('title').text()[0: q('title').text().find('_')]}
        except:
            pass


def update_db_video_name(names):
    global cursor, db
    sql = "update video_info set v_name = %s where v_aid = %s"
    for row in names:
        for v_aid, v_name in row.items():
            try:
                cursor.execute(sql, (v_name, v_aid))
            except:
                db.rollback()
        db.commit()


if __name__ == "__main__":
    video_aids = get_video_aid()
    _names = get_video_name(video_aids)
    update_db_video_name(_names)
    print("Done!!!")
db.close()
