import pymysql
from pyecharts import Liquid

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


def get_all_video_num():
    global cursor
    sql = 'select count(*) from video_info_from_web'
    try:
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        return result
    except:
        db.rollback()


# junk video = without favorite, coin and share
def get_junk_video_num():
    global cursor
    sql = 'select count(*) from video_info_from_web where v_favorite=0 and v_coin=0 and v_share=0'
    try:
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        return result
    except:
        db.rollback()


def junk_video(ratio):
    liquid = Liquid("零收藏硬币分享的视频数占比")
    liquid.add("零收藏硬币分享", [ratio], is_liquid_outline_show=False)
    liquid.render(r'junk_video.html')


if __name__ == "__main__":
    total_num = get_all_video_num()
    junk_num = get_junk_video_num()
    junk_video(junk_num/total_num)
    print(junk_num/total_num)
    print("Done!!!")
