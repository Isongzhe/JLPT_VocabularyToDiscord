import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="s91062013",
    database="JLPT"
)

print('連線成功')

# 建立 cursor 物件
cursor = con.cursor()
# 執行 SQL 語法
cursor.execute("SELECT * FROM N5")
# 確定執行
con.commit()
# 關閉資料庫連線
con.close()