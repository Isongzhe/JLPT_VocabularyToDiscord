import requests
import json
import configparser
import mysql.connector

class Config:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_api_key(self, section, key):
        return self.config[section][key]
    
class DiscordNotifier:
    def __init__(self):
        config = Config('config.ini')
        self.webhook_url = config.get_api_key('DISCORD', 'grammer_URL')

    def send_message(self, level, article_title, article_url, image_url):
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
        self.notifier = DiscordNotifier()

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
                self.notifier.send_message(self.level, article[1], article[2], article[3])

                if not self.test_mode:  # 如果不是在測試模式下運行，則將文章標記為已發送
                    self.mark_as_sent(article[0])  # 將文章標記為已發送
        finally:
            self.cursor.close()
            self.cnx.close()  # 確保數據庫連接被關閉