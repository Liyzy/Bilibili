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

cols = [
    'v_aid', 'v_view', 'v_danmaku', 'v_reply',
    'v_favorite', 'v_coin', 'v_share', 'v_name']
