import pymysql
from pyecharts import WordCloud

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


def get_fans_info():
    global cursor
    sql = 'select user_name,follower from user_info order by follower desc limit 0,30'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        user_names = []
        follower = []
        for result in results:
            user_names.append(result[0])
            follower.append(result[1])
        return [user_names, follower]
    except:
        db.rollback()


def most_fans_up(name, fans):
    wordcloud = WordCloud("B站粉丝最多的30位up主图", "2018-12-31", width=1300, height=620)
    wordcloud.add("", name, fans, word_size_range=[20, 100])
    wordcloud.render(r'most_fans_up.html')


if __name__ == "__main__":
    res = get_fans_info()
    most_fans_up(res[0], res[1])
    print(res[0], res[1])
    print("Done!!!")
