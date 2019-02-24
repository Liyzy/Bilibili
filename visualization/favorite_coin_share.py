import pymysql
from pyecharts import Scatter3D

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


def get_fav_coin_share_info():
    global cursor
    # sql = 'select v_favorite, v_coin, v_share from video_info'
    # 因为大约有50万的视频这三项均为0，为了视觉效果，取一部分数据分析
    sql = 'select v_favorite, v_coin, v_share from video_info_from_web ' \
          'order by v_favorite, v_coin, v_share asc limit 900000,950000'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        video_data = []
        for result in results:
            video_data.append(list(result))
        # print(video_data)
        return video_data
    except:
        db.rollback()


def favorite_coin_share(data):
    scatter3D = Scatter3D("B站视频favorite&coin&share3D散点图", "2018-12-30", width=1400, height=700)
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D.add("收藏+硬币+分享", data, is_visualmap=True, visual_range_color=range_color)
    scatter3D.render(r'fav_coin_share.html')


if __name__ == "__main__":
    v_data = get_fav_coin_share_info()
    favorite_coin_share(v_data)
    print("Done!!!")
