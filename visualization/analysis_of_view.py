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


def get_view_info(lb, ub):
    global cursor
    # sql = 'select count(*) from video_info where v_view > %s and v_view <= %s'
    sql = 'select count(*) from video_info_from_web where v_view > %s and v_view <= %s'
    try:
        cursor.execute(sql, (lb, ub))
        result = cursor.fetchone()
        return result
    except:
        db.rollback()


def view_visualization(columns, view_list):
    pie = Pie("B站视频播放量分布占比饼状图", "播放量分析", width=900, height=700)
    pie.add("播放量", columns, view_list, title_pos='center', radius=[40, 75],
            legend_top='bottom', is_legend_show=True, is_label_show=True)
    pie.render(r'analysis_of_view.html')


if __name__ == "__main__":
    less_five_hundred = get_view_info(0, 500)[0]
    five_hundred_to_one_k = get_view_info(500, 1000)[0]
    one_k_to_five_k = get_view_info(1000, 5000)[0]
    five_k_to_twenty_k = get_view_info(5000, 20000)[0]
    more_than_twenty_k = get_view_info(20000, pow(2, 31))[0]  # mysql中int类型最大值2^31
    cols = ['<500', '500~1000', '1000~5000', '5000~20000', '>20000']
    vl = [less_five_hundred, five_hundred_to_one_k, one_k_to_five_k, five_k_to_twenty_k, more_than_twenty_k]
    view_visualization(cols, vl)
    # print(less_five_hundred, five_hundred_to_one_k, one_k_to_five_k, five_k_to_twenty_k, more_than_twenty_k)
    print("Done!!!")
