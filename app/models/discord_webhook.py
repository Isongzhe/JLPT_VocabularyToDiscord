import requests
import json
import configparser
import mysql.connector
import sys
sys.path.append('D:/GitHub/JLPT_VocabularyToDiscord/app/utils')  # 添加 translator.py 檔案的路徑到 Python 路徑中
from translator import translate_to_chinese  # 導入 translate_to_chinese 函數


class Config:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        # print(self.config.sections())  # 打印所有區段名稱
        # print(dict(self.config['DISCORD']))  # 打印 'DISCORD' 區段的所有鍵和值

    def get_api_key(self, section, key):
        return self.config[section][key]
    
class DiscordNotifier:
    def __init__(self, webhook_type):
        config = Config(r'D:\GitHub\JLPT_VocabularyToDiscord\config.ini')
        self.webhook_url = config.get_api_key('DISCORD', webhook_type)
        print(self.webhook_url)

    def send_grammer(self, level, article_title, article_url, image_url):
        data = {
            'embeds': [{
                'title': f"{level} - {article_title}",
                'url': article_url,
                'image': {
                    'url': image_url
                }
            }]
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(self.webhook_url, data=json.dumps(data), headers=headers)
    

    def send_news(self, date, news_data):
        # 建立一個 embed 物件
        embed = {
            "title": f"{date} - Easy Japanesse新聞",
            "fields": []
        }

        # 為每條新聞添加一個 field
        for i, news_item in enumerate(news_data, start=1):
            for news in news_item['news']:
                # 將 name 翻譯為中文
                name = f"{news['name']}"
                # print(f"Japanese name: {name}")
                # 將 name 翻譯為中文
                translated_name = translate_to_chinese(name)
                translated_name= translated_name
                # print(f"Translated name: {translated_name}")

                jp_name = f"{i}. {name}"
                value = f"[{translated_name}]({news['webURL']})"
                # print(f"Value: {value}")
                
                embed["fields"].append({
                    "name": jp_name,
                    "value": value
                })

        # 將 embed 物件轉換為 JSON 字串
        for field in embed["fields"]:
            field["name"] = field["name"].replace('\n', '').replace(' ', '').replace('\u3000', ' ')
            field["value"] = field["value"].replace('\n', '').replace(' ', '').replace('\u3000', ' ')
            # 檢查欄位長度
            if len(field["name"]) > 1024 or len(field["value"]) > 1024:
                print(f"Field '{field['name']}' or its value is too long.")

        # # 將 embed 物件轉換為 JSON 字串
        # data = json.dumps({"embeds": [embed]}, ensure_ascii=False)

        # print("Sending the following data:")
        # print(data)

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self.webhook_url, data=json.dumps({"embeds": [embed]}, ensure_ascii=False), headers=headers)
            response.raise_for_status()
            print("Response from Discord:")
            print(response.text)
        
        except requests.exceptions.RequestException as err:
            print(f"HTTP error occurred: {err}")
            print(f"Response text: {response.text}")
        

#測試預覽: https://leovoel.github.io/embed-visualizer/

class ArticleSender:
    def __init__(self, level, db_settings, test_mode=False):
        self.cnx = mysql.connector.connect(
            host=db_settings["host"],
            user=db_settings["user"],
            password=db_settings["password"],
            database=db_settings["db"],
            charset=db_settings["charset"]
        )
        self.cursor = self.cnx.cursor()
        self.level = level
        self.test_mode = test_mode
        self.notifier = DiscordNotifier('grammar_URL')

    def get_unsent_article(self):
        query = "SELECT * FROM grammararticle WHERE is_sent = 0 AND level = %s LIMIT 1"
        self.cursor.execute(query, (self.level,))
        results = self.cursor.fetchone()
        return results if results else None

    def mark_as_sent(self, article_id):
        query = "UPDATE grammararticle SET is_sent = 1 WHERE id = %s"
        self.cursor.execute(query, (article_id,))
        self.cnx.commit()

    def send_article(self):
        try:
            article = self.get_unsent_article()
            if article:
                self.notifier.send_grammer(self.level, article[1], article[2], article[3])

                if not self.test_mode:  # 如果不是在測試模式下運行，則將文章標記為已發送
                    self.mark_as_sent(article[0])  # 將文章標記為已發送
        finally:
            self.cursor.close()
            self.cnx.close()  # 確保數據庫連接被關閉