import threading
import time
from concurrent import futures

import pymysql
import requests

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

total = 1
result = []
lock = threading.Lock()

# 连接数据库，创建游标对象
db = pymysql.connect(**conn)
cursor = db.cursor()


def run(url):
    # 启动爬虫
    global total, result
    req = requests.get(url, headers=headers, timeout=6).json()
    time.sleep(0.5)  # 延迟，避免太快 ip 被封
    try:
        data = req['data']
        if data['view'] != "--" and data['aid'] != 0:
            video = (
                data['aid'],  # 视频编号
                data['view'],  # 播放量
                data['danmaku'],  # 弹幕数
                data['reply'],  # 评论数
                data['favorite'],  # 收藏数
                data['coin'],  # 硬币数
                data['share'],  # 分享数
                ""              # 视频名，后期获取
            )
            with lock:
                result.append(video)
                if total % 100 == 0:
                    print(total)
                total += 1
    except:
        pass


def create_db():
    # 创建数据库
    global cursor
    # cursor.execute('drop table if exists video_info')  # 如果存在video_info表，则删除
    cursor.execute("""create table if not exists video_info
                   (v_aid int primary key,
                    v_view int,
                    v_danmaku int,
                    v_reply int,
                    v_favorite int,
                    v_coin int,
                    v_share int,
                    v_name varchar(255))""")


def save_db():
    # 将数据保存至本地
    global result, cursor, db, total
    sql = "insert into video_info values(%s, %s, %s, %s, %s, %s, %s, %s);"
    for row in result:
        try:
            cursor.execute(sql, row)
        except:
            db.rollback()
    db.commit()
    result = []


if __name__ == "__main__":
    create_db()
    print("Bilibili crawler running...")
    for i in range(70, 80):
        begin = 10000 * i
        urls = ["https://api.bilibili.com/x/web-interface/archive/stat?aid={}".format(j)
                for j in range(begin, begin + 10000)]
        with futures.ThreadPoolExecutor(64) as executor:
            executor.map(run, urls)
        save_db()
    print("The crawler ends, a total of {} data crawled for you.".format(total))
    db.close()
