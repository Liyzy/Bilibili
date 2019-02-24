import pyecharts
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
print("Database has connected!")
cursor = db.cursor()


def get_aid_view_info():
    global cursor
    # sql = 'select v_aid, v_view from video_info order by v_aid asc'
    sql = 'select v_aid, v_view from video_info_from_web order by v_aid asc'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        aid, view = [[], []]
        for result in results:
            aid.append(result[0])
            view.append(result[1])
        # print(aid)
        # print(view)
        return [aid, view]
    except:
        db.rollback()


def aid_view_visualization(aid, view):
    bar = pyecharts.Bar("B站视频aid与播放量view的关系", "2018-12-29", width=1400, height=700)
    bar.add("播放量", aid, view, title_pos='center',
            legend_top='bottom', is_legend_show=True, is_label_show=False,
            # 默认为 X 轴，横向
            is_datazoom_show=True,
            datazoom_type="slider",
            # 新增额外的 dataZoom 控制条，纵向
            is_datazoom_extra_show=True,
            datazoom_extra_type="slider")
    bar.render(r'relationship_aid_view.html')


if __name__ == "__main__":
    res = get_aid_view_info()
    aid_view_visualization(res[0], res[1])
    print("Done!!!")
