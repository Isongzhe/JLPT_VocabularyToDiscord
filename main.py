# from app.models.manageDB import DatabaseManager
from app.models.discord_webhook import DiscordNotifier, ArticleSender
import os
# from app.utils.scaper_news import ScraperNews, WebDriver
import subprocess
import json


def send_grammar_article():
    # Database settings
    db_settings = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "s91062013",
        "db": "JLPT",
        "charset": "utf8"
    }
    # 定義等級的順序
    levels = ['N3', 'N4']

    # 檔案路徑
    file_path = r'D:\GitHub\JLPT_VocabularyToDiscord\app\utils\current_level.txt'

    # 如果檔案存在，讀取當前的等級
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            current_level = file.read().strip()
    else:
        # 如果檔案不存在，則預設為 N3
        current_level = 'N3'

    # 建立一個 ArticleSender 物件，發送當前等級的文章
    article_sender = ArticleSender(current_level, db_settings, test_mode=False)
    article_sender.send_article()

    # 更新等級為下一個等級
    next_level = levels[(levels.index(current_level) + 1) % len(levels)]

    # 將下一個等級寫入檔案
    with open(file_path, 'w') as file:
        file.write(next_level)

def send_news_article():

    # # 執行 scaper_news.py 檔案
    # subprocess.run(['python', 'D:/GitHub/JLPT_VocabularyToDiscord/app/utils/scaper_news.py'])
    
    # 讀取生成的 JSON 檔案
    with open('D:/GitHub/JLPT_VocabularyToDiscord/app/utils/EasyJapan_news.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)
        # print(news_data)
    # 從讀取的資料中取得第一個物件的 date 的值
    date = news_data[0]['date']

    # print(date)
    # 建立一個 DiscordNotifier 物件，發送新聞
    news_notifier = DiscordNotifier('news_URL')
    news_notifier.send_news(date, news_data)

def main():
    send_grammar_article()
    send_news_article()

if __name__ == "__main__":
    main()