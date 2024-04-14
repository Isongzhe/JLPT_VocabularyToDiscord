import json
import pymysql

# 資料庫連線設定
db_settings = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "s91062013",
    "db": "JLPT",
    "charset": "utf8"
}

try:
    # 建立連線
    conn = pymysql.connect(**db_settings)

    # 建立游標
    with conn.cursor() as cursor:
        # 讀取每一個 JSON 檔案
        for level in ['N1', 'N2', 'N3', 'N4', 'N5']:
            filename = f'D:\\GitHub\\JLPT_VocabularyToDiscord\\scraper_file\\{level}_grammer.json'
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 對每一個 JSON 物件，將其欄位的值插入到資料庫的表格中
                for article in data:
                    cursor.execute(
                        "INSERT INTO grammarArticle (name, webURL, imageURL, level, is_sent) VALUES (%s, %s, %s, %s, %s)",
                        (article['name'], article['webURL'], article['imageURL'], article['level'], article['number'])
                    )
                # 提交事務
                conn.commit()


except Exception as ex:
    print(ex)

finally:
    # 關閉連線
    if conn:
        conn.close()